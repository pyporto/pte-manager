from typing import Iterator
from pte import settings
from requests import Session
from pte.events import Event
from pte.utils import get_date

meetup = Session()
meetup.headers['Authorization'] = settings.MEETUP_API_KEY


def scrape() -> Iterator[Event]:
    for community in settings.MEETUP_COMMUNITIES:
        yield from scrape_community(community)


def scrape_community(community: str) -> Iterator[Event]:
    url = f'https://api.meetup.com/{community}/events'
    params = {
        'fields': 'plain_text_no_images_description',
    }
    resp = meetup.get(url, params=params)
    resp.raise_for_status()
    events = resp.json()
    for ev_dict in events:
        ev_date = get_date(ev_dict["local_date"])
        descrption = ev_dict['plain_text_no_images_description']
        ev = Event(
            id=f'{community}-{ev_dict["id"]}',
            url=ev_dict['link'],
            name=ev_dict['name'],
            description=descrption.splitlines(True),
            start_date=ev_date,
            end_date=ev_date,
            location=ev_dict['venue']['name'],
            rrule=None,
        )
        yield ev
