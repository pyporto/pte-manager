import requests
import datetime
from typing import Iterator
from pte import settings
from pte.events import Event

eventbrite = requests.Session()
eventbrite.headers = {'Authorization': f'Bearer {settings.EVENTBRITE_API_TOKEN}'}

# "Science and Tech": https://www.eventbriteapi.com/v3/categories/102
CATEGORY_ID = 102
BASE_URL = 'https://www.eventbriteapi.com/v3'


def scrape() -> Iterator[Event]:
    url = f'{BASE_URL}/events/search'
    params = {
        'sort_by': 'date',
        'location.address': 'Porto',
        'location.within': '50km',
        'categories': CATEGORY_ID,
        'start_date.range_start':  datetime.date.today().strftime('%FT00:00:00'),
        'include_all_series_instances': 'true',
    }
    resp = eventbrite.get(url, params=params)
    resp.raise_for_status()
    for ev_dict in resp.json()['events']:
        ev = eventbrite_to_event(ev_dict)
        yield ev


def eventbrite_to_event(ev_dict: dict) -> Event:
    start_date = datetime.datetime.strptime(
        ev_dict['start']['local'], '%Y-%m-%dT%H:%M:%S').date()
    end_date = datetime.datetime.strptime(
        ev_dict['end']['local'], '%Y-%m-%dT%H:%M:%S').date()
    id = f'eventbrite-{ev_dict["id"]}'

    venue_resp = eventbrite.get(f'{BASE_URL}/venues/{ev_dict["venue_id"]}/')
    venue_resp.raise_for_status()

    location = venue_resp.json()['name']
    if not location:
        location = venue_resp.json()['address']['localized_address_display']

    return Event(id=id,
                 url=ev_dict['url'],
                 name=ev_dict['name']['text'],
                 description=ev_dict['description']['text'].splitlines(True),
                 start_date=start_date,
                 end_date=end_date,
                 location=location,
                 rrule=None)
