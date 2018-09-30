from typing import Iterator
from requests_html import HTMLSession
from dateutil.parser import parse
from slugify import slugify

from pte.events import MiscEvent
from pte.scrapers import core

session = HTMLSession()


def scrape() -> Iterator[MiscEvent]:
    resp = session.get(
        'https://www.timeanddate.com/holidays/portugal/',
        headers={
            'Accept-Language': 'en-US',
        })
    resp.raise_for_status()
    i = 0
    while True:
        rows = resp.html.find(f'#tr{i}')
        if not rows:
            break
        row = rows[0]
        date_str = row.find('th')[0].text
        date = parse(date_str)
        td = row.find('td')[1]
        holiday_name = td.text
        url = list(td.absolute_links)[0]
        event_id = slugify(f'timedate-{date:%Y}-{holiday_name}')
        yield MiscEvent(
            id=event_id,
            url=url,
            name=holiday_name,
            description=[],
            start_date=date,
            end_date=date,
        )
        i += 1


core.register('timedate', scrape)
