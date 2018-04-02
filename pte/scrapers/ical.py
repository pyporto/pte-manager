from typing import Iterator
from icalendar import Calendar
import requests
from slugify import slugify

from pte import settings
from pte.events import Event
from pte.scrapers import core


def scrape() -> Iterator[Event]:
    for feed_name, feed_url in settings.ICAL_FEEDS:
        yield from scrape_feed(feed_name, feed_url)


def scrape_feed(feed_name, feed_url) -> Iterator[Event]:
    resp = requests.get(feed_url)
    resp.raise_for_status()
    cal = Calendar.from_ical(resp.text)
    for ev in cal.walk():
        if ev.name == "VEVENT":
            start_date = ev['DTSTART'].dt
            end_date = ev['DTEND'].dt
            event_id = slugify(f'{feed_name}-{str(ev["UID"])}')
            url = ev['URL']
            name = str(ev['SUMMARY'])
            description = str(ev['DESCRIPTION']).splitlines(True)
            yield Event(
                id=event_id,
                url=url,
                name=name,
                description=description,
                start_date=start_date,
                end_date=end_date,
            )


core.register(scrape)
