from typing import Callable, Iterator, Dict
from pte import events


Scraper = Callable[[], Iterator[events.GenericEvent]]


scrapers = {}  # type: Dict[str, Scraper]


def register(name: str, scraper: Scraper):
    scrapers[name] = scraper


def run_all():
    for scraper in scrapers.values():
        run_scraper(scraper)


def run_scraper(name: str):
    """
    Main function to update the list of events from the remote
    source.

    Takes the scraper name. The callable of scraper doesn't accept any
    parameters and return an iterator of events, read every instance from the
    scraper and tries to create or update a description of the event in
    MODEL_STORAGE_ROOT
    """
    scraper = scrapers[name]
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
