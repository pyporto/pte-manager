import hashlib
import datetime

from requests import Session
from pte import settings, events
from pte.gcal.access import get_access_token


BASE_URL = 'https://www.googleapis.com/calendar/v3/calendars'


sess = Session()
sess.headers['Authorization'] = f'Bearer {get_access_token()}'


class GenericGCalSynchronizer:

    gcal_id = None
    event_class = None
    event_color = None

    def clear(self):
        events_url = f'{BASE_URL}/{self.gcal_id}/events'
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

    def sync(self):
        url = f'{BASE_URL}/{self.gcal_id}/events'
        local_events = self.get_local_events()
        remote_events = self.get_remote_events()

        # sync events, existing locally
        for event_id, event in local_events.items():
            gcal_event = self.event_to_gcal(event)
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

    def get_local_events(self):
        ret = {}
        today = datetime.date.today()
        for ev in self.event_class.get_all():
            if ev.relevant and ev.end_date >= today:
                ret[self.get_gcal_id(ev)] = ev
        return ret

    def get_remote_events(self):
        url = f'{BASE_URL}/{self.gcal_id}/events'
        params = {
            'maxResults': 2500,
        }
        resp = sess.get(url, params=params)
        resp.raise_for_status()
        return {item['id']: item for item in resp.json()['items']}

    def event_to_gcal(self, event: events.GenericEvent):
        gcal_id = self.get_gcal_id(event)
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
            'colorId': self.event_color,
        }
        if event.rrule:
            gcal_event['recurrence'] = [event.rrule]
        return gcal_event

    def get_gcal_id(self, ev: events.GenericEvent):
        return hashlib.sha1(ev.id.encode('ascii')).hexdigest()


class GCalSynchronizer(GenericGCalSynchronizer):
    gcal_id = settings.GCAL_ID
    event_class = events.Event
    event_color = 10  # green


class MiscGCalSynchronizer(GenericGCalSynchronizer):
    gcal_id = settings.MISC_GCAL_ID
    event_class = events.MiscEvent
    event_color = 8  # grey


def sync():
    GCalSynchronizer().sync()
    MiscGCalSynchronizer().sync()
