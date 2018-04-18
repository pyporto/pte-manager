How to scrape
-------------


```sh
./manage.py scrape
```

How to update Google Calendar
-----------------------------

```sh
./manage.py sync_gcal
```


The overall workflow
--------------------

Update the Facebook key in .env against
https://developers.facebook.com/tools/explorer/ and then run


```
./manage.py scrape
./manage.py status
./manage.py sync_github
./manage.py sync_gcal
```
