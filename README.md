# normalize_events
normalize_events takes events from the following sources and creates a normalizes the data in one API endpoint:

* [Eventbrite](http://developer.eventbrite.com/)
* [Brown Paper Tickets](https://www.brownpapertickets.com/developer/index.html)
* [Eventful](http://api.eventful.com/)
* [Meetup](http://www.meetup.com/meetup_api/)

Coming soon...

* FaceBook (still working on this one)
* Universe
* SeatGeek

[Working example.](normalizevents.us/api/v1.0/events)

# Setup

Clone the repository.

```bash
git clone git@github.com:adamyala/normalize_events.git
```

Install all dependencies.

```bash
cd normalize_events && pip install -r requirements.txt
```

Make sure PostgreSQL is running. Default URI is:
```
postgres://localhost:5432/events
```

Run:
```
./cron.sh
```

`cron.sh` hits all the sources for events and can be setup as a cron every few hours.

NOTE: Eventbrite limits API hits every 8 hours. Pulling all events at first may take multiple runs.

# Use

The API endpoints are `/events` and `/eventlogs`. Currently the API uses Basic HTTP Authorization.

Available params for `/events`:

* `/events?event_id=X`
    * where `X` is your internal id for that event record
* `/events?city=X`
    * where `X` is the desired city for returned events
* `/events?startDate=X`, `/events?endDate=X`, `/events?createdDateStart=X`, `/events?createdDateEnd=X`
    * where `X` is any date in the `YYYY-MM-DD` or `YYYY-M-D` format
    * `startDate` specifies the earliest date the returned events will occur
    * `endDate` specifies the latest date the returned events will occur
    * `createdDateStart` specifies the earliest date the returned events were added to the database
    * `createdDateEnd` specifies the latest date the returned events were added to the database
    
# Full Example

`normalizevents.us/api/v1.0/events?city=Chicago&startDate=2015-12-1&endDate=2015-12-31&createdDateStart=2015-11-1&createdDateEnd=2015-11-30`

The above example returns all events occurring in December in Chicago that were added to the system in the month of November.