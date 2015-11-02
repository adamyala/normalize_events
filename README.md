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
