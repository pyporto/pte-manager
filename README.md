How to scrape
-------------


```python
from pte.scrapers import core, eventbrite, meetup, sapo
core.scrape(eventbrite.scrape)
core.scrape(meetup.scrape)
core.scrape(sapo.scrape)
```

How to update Google Calendar
-----------------------------

```python
from pte.gcal.sync import sync
sync()
```
