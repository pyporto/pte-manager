import asyncio
import datetime
import logging
from typing import Iterator

from asgiref.sync import async_to_sync
from pte import settings
from pte.events import Event
from pte.scrapers import core
from pte.utils import get_date
from pyppeteer import launch
from pyppeteer.browser import Browser
from pyppeteer.network_manager import Response

logger = logging.getLogger(__name__)

BROWSER_MAX_PAGES = 8
BROWSER_HEADLESS = True


@async_to_sync
async def scrape() -> Iterator[Event]:
    browser = await launch(headless=BROWSER_HEADLESS)
    promises = []

    sem = asyncio.Semaphore(BROWSER_MAX_PAGES)
    for page in settings.FACEBOOK_PAGES:
        catcher = EventsCatcher(browser, page, sem)
        promises.append(catcher.get_events())

    try:
        done, _ = await asyncio.wait(promises)
    finally:
        await browser.close()

    ret = []
    for task in done:
        ret += task.result()
    return ret


class EventsCatcher(object):

    GRAPHQL_URL = 'https://www.facebook.com/api/graphql/'

    def __init__(self, browser: Browser, page_name: str,
                 semaphore: asyncio.Semaphore):
        self.browser = browser
        self.page_name = page_name
        self.semaphore = semaphore
        self.resp_promises = []
        self.too_old_threshold = datetime.date.today() - datetime.timedelta(
            days=90)

    async def get_events(self):
        async with self.semaphore:
            page = await self.browser.newPage()
            page.on('response', self.on_response)
            await page.goto(self.get_page_url())
            ret = await self.parse_responses()
            await page.close()
            return ret

    def get_page_url(self):
        return 'https://www.facebook.com/{}/events'.format(self.page_name)

    def on_response(self, response: Response):
        if response.url == self.GRAPHQL_URL:
            self.resp_promises.append(response.json())

    async def parse_responses(self):
        ret = []
        for resp_promise in self.resp_promises:
            resp = await resp_promise

            try:
                events = resp['data']['page']['upcoming_events']
            except KeyError:
                try:
                    events = resp['data']['page']['past_events']
                except KeyError:
                    continue

            logger.info('Facebook parser %s found %s events', self.page_name,
                        len(events['edges']))
            for edge in events['edges']:
                ev = self.dict_to_event(edge['node'])
                if ev.start_date > self.too_old_threshold:
                    ret.append(ev)
        return ret

    def dict_to_event(self, ev_dict: dict) -> Event:
        time_range = ev_dict['time_range']
        start_date = get_date(time_range['start'][:10])
        if 'end_time' in time_range:
            end_date = get_date(time_range['end_time'][:10])
        else:
            end_date = start_date

        event_place = ev_dict.get('event_place') or {}
        location = event_place.get('name') or event_place.get('contextual_name')

        ev = Event(
            id=f'fb-{self.page_name}-{ev_dict["id"]}',
            url=f'https://www.facebook.com/events/{ev_dict["id"]}/',
            name=ev_dict['name'],
            description=ev_dict.get('description', '').splitlines(True),
            start_date=start_date,
            end_date=end_date,
            location=location,
            rrule=None,
        )
        return ev


core.register('facebook', scrape)
