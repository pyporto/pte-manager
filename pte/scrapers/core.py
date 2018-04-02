from typing import Callable, Iterator, List
from pte import events


Scraper = Callable[[], Iterator[events.GenericEvent]]


scrapers = []  # type: List[Scraper]


def register(scraper: Scraper):
    scrapers.append(scraper)


def run_all():
    for scraper in scrapers:
        run_scraper(scraper)


def run_scraper(scraper: Scraper):
    """
    Main function to update the list of events from the remote
    source.

    Takes the "scraper" callable, which doesn't accept any parameters and
    return an iterator of events, read every instance from the scraper and
    tries to create or update a description of the event in MODEL_STORAGE_ROOT
    """
    for ev in scraper():
        orig_ev = ev.__class__.get_by_id(ev.id)
        if orig_ev:
            update(orig_ev, ev)
            orig_ev.save()
        else:
            ev.save()


def update(target: events.GenericEvent, source: events.GenericEvent):
    for k, v in source.__dict__.items():
        if k != 'relevant':
            target.__dict__[k] = v
