# Porto Tech Events Manager

Before COVID, when offline events were still a thing, we used this application to keep track of all the tech and non-tech relevant events happening around Porto. To store events, we used a GitHub repository [pyporto/porto-tech-events](https://github.com/pyporto/porto-tech-events/), and in addition to that, we exported data in Google Calendar.

The primary goal of the project was to help community organizers to choose the best time for their events and avoid overlaps with other occurrences.

In addition to tech events, we scraped and populated the database with so-called "misc events," those that have nothing to do with technology but should be taken into account while selecting the meeting time, such as national holidays or football matches.


## Project Architecture

- The module `pte.scrapers` contains the list of scrapers. Each scraper is a module that should contain the function `scrape()`, returning an iterator of event objects. The module should be initialized with hardcoded values or environment.
- The module `pte.gcal` provides a Google Calendar integration to export events in a publicly available calendar.


## How to scrape


```sh
./manage.py scrape
```

## How to update Google Calendar


```sh
./manage.py sync-gcal
```


## The overall workflow

Update the Facebook key in .env against
https://developers.facebook.com/tools/explorer/ and then run


```
./manage.py scrape
./manage.py status
./manage.py sync_github
./manage.py sync_gcal
```
