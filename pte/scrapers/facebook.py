import datetime
from typing import Iterator
from pte import settings
from requests import Session
from pte.events import Event
from pte.utils import get_date
from pte.scrapers import core

sess = Session()
sess.headers['Authorization'] = f'Bearer {settings.FACEBOOK_ACCESS_TOKEN}'


def scrape() -> Iterator[Event]:
    for page in settings.FACEBOOK_PAGES:
        yield from scrape_page_events(page)


def scrape_page_events(page: str) -> Iterator[Event]:
    too_old_threshold = datetime.date.today() - datetime.timedelta(days=30)

    resp = sess.get(get_page_url(page))
    resp.raise_for_status()
    events = resp.json()['events']['data']
    for ev_dict in events:
        start_date = get_date(ev_dict['start_time'][:10])
        if 'end_time' in ev_dict:
            end_date = get_date(ev_dict['end_time'][:10])
        else:
            end_date = start_date
        if start_date < too_old_threshold:
            continue

        ev = Event(
            id=f'fb-{page}-{ev_dict["id"]}',
            url=f'https://www.facebook.com/events/{ev_dict["id"]}/',
            name=ev_dict['name'],
            description=ev_dict.get('description', '').splitlines(True),
            start_date=start_date,
            end_date=end_date,
            location=ev_dict.get('place', {}).get('name', None),
            rrule=None,
        )
        yield ev


def get_page_url(page):
    url = (f'https://graph.facebook.com/v2.12/{page}?'
           'fields=events{name,description,start_time,end_time,id,place}')
    return url


core.register(scrape)
