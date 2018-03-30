import os
import json
import datetime
from dataclasses import dataclass, field, asdict
from pte import settings
from typing import Iterator, List, Text

from pte.utils import get_date


@dataclass
class GenericEvent:
    """
    Generic class for a certain type of event. There are two subclasses for
    it -- the "Event" (something relevant to the tech community) and
    the "MiscEvent" (an event which is not relevant to the tech community,
    but can affect the attendance, something like a holiday or a big football
    game, so it's better to keep an eye on it)
    """
    id: Text
    url: Text
    name: Text
    description: List[Text]
    start_date: datetime.date
    end_date: datetime.date
    location: Text = None
    rrule: Text = None
    relevant: bool = True
    model_root: str = field(init=False)

    def get_description(self):
        return ''.join(self.description)

    def get_dict(self):
        ret = asdict(self)
        ret.pop('id')
        ret.pop('model_root')
        ret['start_date'] = ret['start_date'].strftime('%Y-%m-%d')
        ret['end_date'] = ret['end_date'].strftime('%Y-%m-%d')
        if self.relevant:
            ret.pop('relevant')
        return ret

    def save(self):
        filename = self.get_filename()
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'wt') as fd:
            json.dump(self.get_dict(), fd, indent=2, sort_keys=True)

    def get_filename(self):
        return os.path.join(self.get_model_root(),
                            self.id + '.json')

    @classmethod
    def get_by_id(cls, event_id: str) -> 'GenericEvent':
        full_filename = os.path.join(cls.get_model_root(),
                                     event_id + '.json')
        if os.path.isfile(full_filename):
            return cls._read_from_file(full_filename)

    @classmethod
    def get_all(cls) -> 'Iterator[GenericEvent]':
        for filename in os.listdir(cls.get_model_root()):
            if not filename.endswith('.json'):
                continue
            ev_id, _ = os.path.splitext(filename)
            yield cls.get_by_id(ev_id)

    @classmethod
    def get_model_root(cls):
        return os.path.join(settings.MODEL_STORAGE_ROOT,
                            cls.model_root)

    @classmethod
    def _read_from_file(cls, filename) -> 'GenericEvent':
        event_id = os.path.basename(filename)
        event_id, _ = os.path.splitext(event_id)
        with open(filename) as fd:
            ev = json.load(fd)
            ev['id'] = event_id
            ev['start_date'] = get_date(ev['start_date'])
            ev['end_date'] = get_date(ev['end_date'])
            return cls(**ev)


class Event(GenericEvent):
    model_root = 'events'


class MiscEvent(GenericEvent):
    model_root = 'misc'
