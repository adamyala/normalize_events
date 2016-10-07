# normalize_events

[![Code Issues](https://www.quantifiedcode.com/api/v1/project/e449d11d17f74ceb9dcaf2d03b589775/badge.svg)](https://www.quantifiedcode.com/app/project/e449d11d17f74ceb9dcaf2d03b589775)

normalize_events takes events from the following sources and normalizes the data in one API endpoint:

* [Eventbrite](http://developer.eventbrite.com/)
* [Brown Paper Tickets](https://www.brownpapertickets.com/developer/index.html)
* [Eventful](http://api.eventful.com/)
* [Meetup](http://www.meetup.com/meetup_api/)
* [Universe](https://www.universe.com/)

Coming soon...

* FaceBook (still working on this one)

[Working example.](http://normalizevents.us/api/v1.0/events)

# Setup

## Local Development - Vagrant

This method requires [VirtualBox](https://www.virtualbox.org/wiki/Downloads), [Vagrant](https://www.vagrantup.com/downloads.html), and [Ansible](http://docs.ansible.com/ansible/intro_installation.html)

1. Clone the repository with `git clone git@github.com:adamyala/normalize_events.git`
1. `cd` into the directory
1. Run `git submodule update --init --recursive` to pull in ansible roles
1. Add your API keys to all the token fields in `config.py`
1. Run `vagrant up`
1. The API can be accessed at `127.0.0.1:4567`

The Vagrant machine will be using your local files so any changes will be reflected.

NOTE: Eventbrite limits API hits every 8 hours. Pulling all events at first may take multiple runs.

## Local Development - Manually

Clone the repository.

```
git clone git@github.com:adamyala/normalize_events.git
```

Install all dependencies.

```
cd normalize_events && pip install -r requirements.txt
```

Make sure PostgreSQL is running and that a database called `events` exists. Default URI is:

```
postgres://localhost:5432/events
```

In `config.py`, set the `CATEGORY` variable to the event category you'd like to download.

Then run `python models.py` so the SQLAlchemy engine creates all required tables.

Before loading the database you have to go into `config.py` and set the API tokens for each of the APIs you'd like to use. Then run:
```
./cron.sh
```

`cron.sh` hits all the uncommented sources for events and can be setup as a cron every few hours.

NOTE: Eventbrite limits API hits every 8 hours. Pulling all events at first may take multiple runs.

## Troubleshooting

NOTE: If `psycopg2` fails to install with the error "unable to install psycopg2 because pg_config executable not found", and you're using the [Postgress.app](http://postgresapp.com/) on MacOS, the path to Postgress.app has to be added to the virtual environment. Try the below.

```
# Activate your virtual environment
source /path/to/you/env/activate
# Add Postgress to your virtual environment. This is only temporary, so it'll disappear as soon as you deactivate the virtual environment.
PATH="/Applications/Postgres.app/Contents/Versions/YOUR_VERSION_NUMBER/bin:$PATH"
# Install psycopg2
pip install psycopg2
```

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

`http://normalizevents.us/api/v1.0/events?city=Chicago&startDate=2015-12-1&endDate=2015-12-31&createdDateStart=2015-11-1&createdDateEnd=2015-11-30`

The above example returns all events occurring in December in Chicago that were added to the system in the month of November.
