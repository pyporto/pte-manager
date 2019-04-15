import datetime
import hashlib
import logging
import time

from requests import Session

from pte import events, settings
from pte.gcal.access import get_access_token

BASE_URL = 'https://www.googleapis.com/calendar/v3/calendars'

logger = logging.getLogger(__name__)
sess = Session()
sess.headers['Authorization'] = f'Bearer {get_access_token()}'


class GenericGCalSynchronizer:

    gcal_id = None
    event_class = None
    event_color = None

    def clear(self):
        logger.info('Clear Google Calendar')
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
        logger.info('Sync locally existing events')
        for event_id, event in local_events.items():
            logger.debug('Sync event %s', event_id)
            gcal_event = self.event_to_gcal(event)
            if event_id in remote_events.keys():
                resp = sess.put(url + '/' + event_id, json=gcal_event)
            else:
                resp = sess.post(url, json=gcal_event)
            process_http_response(resp)
            time.sleep(0.2)

        # remove events which don't exist locally anymore
        logger.info('Remove locally non-existent events')
        for event_id in remote_events.keys():
            logger.debug('Delete remote event %s', event_id)
            if event_id not in local_events.keys():
                resp = sess.delete(url + '/' + event_id)
                process_http_response(resp)
                time.sleep(0.2)

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


def process_http_response(resp):
    """
    Helper function which returns a bit more information on
    GCal sync failure
    """
    if resp.status_code != 200:
        json_err = resp.json()
        err_reason = json_err['error']['errors'][0]['reason']
        err_text = json_err['error']['message']
        logger.error(f'GCal returns non-ok status code: '
                     f'{err_text} ({err_reason})')
    resp.raise_for_status()
