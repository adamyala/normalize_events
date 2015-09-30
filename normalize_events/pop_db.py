# from lib.feeds.test_feed import TestClient
from lib.feeds.eventbrite import EventbriteClient
from lib.feeds.meetup import MeetupClient
from lib.feeds.brownpapertickets import BPTClient
from lib.feeds.eventful import EventfulClient
from lib.pop_db import PopDb
from config import *
from lib.maps import MapClient


def main():
    map_client = MapClient(CLIENT_GM['url'], CLIENT_GM['token'])
    pop_db = PopDb(
        [
            # TestClient(),
            # BPTClient(CLIENT_BPT['url'], CLIENT_BPT['token'], CLIENT_BPT['source']),
            MeetupClient(CLIENT_MU['url'], CLIENT_MU['token'], CLIENT_MU['source']),
            # EventbriteClient(CLIENT_EB['url'], CLIENT_EB['token'], CLIENT_EB['source']),
            # EventfulClient(CLIENT_EF['url'], CLIENT_EF['token'], CLIENT_EF['source']),
        ]
    )
    pop_db.set_events()
    for event in pop_db.events:
        pop_db.insert_event(event)
        if CLIENT_GM['on']:
            map_client.download_map(event.get_address(), event.event_id)
    return

main()
