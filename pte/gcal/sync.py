import hashlib
import datetime

import itertools
from requests import Session
from pte import settings, events
from pte.gcal.access import get_access_token


BASE_URL = 'https://www.googleapis.com/calendar/v3/calendars'


sess = Session()
sess.headers['Authorization'] = f'Bearer {get_access_token()}'


def clear():
    events_url = f'{BASE_URL}/{settings.GCAL_ID}/events'
    total_events = 0
    while True:
        resp = sess.get(events_url)
        resp.raise_for_status()
        json_resp = resp.json()
        for ev in json_resp['items']:
            resp = sess.delete(events_url + '/' + ev['id'])
            resp.raise_for_status()
            total_events += 1
        if not json_resp.get('nextPageToken'):
            break
    return total_events


def sync():
    url = f'{BASE_URL}/{settings.GCAL_ID}/events'
    local_events = _get_local_events()
    remote_events = _get_remote_events()

    # sync events, existing locally
    for event_id, event in local_events.items():
        gcal_event = _event_to_gcal(event)
        if event_id in remote_events.keys():
            resp = sess.put(url + '/' + event_id, json=gcal_event)
        else:
            resp = sess.post(url, json=gcal_event)
        resp.raise_for_status()

    # remove events which don't exist locally anymore
    for event_id in remote_events.keys():
        if event_id not in local_events.keys():
            resp = sess.delete(url + '/' + event_id)
            resp.raise_for_status()


def _get_local_events():
    ret = {}
    today = datetime.date.today()
    ee = itertools.chain(events.Event.get_all(),
                         events.MiscEvent.get_all())
    for ev in ee:
        if ev.relevant and ev.end_date >= today:
            ret[get_gcal_id(ev)] = ev
    return ret


def _get_remote_events():
    url = f'{BASE_URL}/{settings.GCAL_ID}/events'
    params = {
        'maxResults': 2500,
    }
    resp = sess.get(url, params=params)
    resp.raise_for_status()
    return {item['id']: item for item in resp.json()['items']}


def _event_to_gcal(event: events.GenericEvent):
    gcal_id = get_gcal_id(event)
    gcal_event = {
        'id': gcal_id,
        'start': {
            'date': event.start_date.strftime('%F'),
        },
        'end': {
            'date': event.end_date.strftime('%F'),
        },
        'location': event.location,
        'source': {
            'url': event.url,
        },
        'status': 'confirmed',
        'summary': event.name,
        'description': event.description,
        'colorId': get_gcal_color_id(event),
    }
    if event.rrule:
        gcal_event['recurrence'] = [event.rrule]
    return gcal_event


def get_gcal_id(ev: events.GenericEvent):
    return hashlib.sha1(ev.id.encode('ascii')).hexdigest()


def get_gcal_color_id(ev: events.GenericEvent):
    if isinstance(ev, events.Event):
        return 10  # green
    elif isinstance(ev, events.MiscEvent):
        return 8  # grey
