from lib.feeds.test_feed import TestClient
from lib.feeds.eventbrite import EventbriteClient
from lib.feeds.meetup import MeetupClient
from lib.feeds.brownpapertickets import BPTClient
from lib.feeds.universe import UniverseClient
from lib.feeds.eventful import EventfulClient
from lib.pop_db import PopDb
from config import *
from lib.maps import MapClient


def main():
    map_client = MapClient()
    pop_db = PopDb([
        # TestClient(),
        BPTClient(CLIENT_BPT['url'], CLIENT_BPT['token']),
        MeetupClient(CLIENT_MU['url'], CLIENT_MU['token']),
        EventbriteClient(CLIENT_EB['url'], CLIENT_EB['token']),
        EventfulClient(CLIENT_EF['url'], CLIENT_EF['token']),
        UniverseClient(CLIENT_UNI['url'])
    ])
    pop_db.set_events()
    for event in pop_db.events:
        pop_db.insert_event(event)
        if CLIENT_GM['on']:
            map_client.download_map(event.get_address(), event.event_id)
    return

main()
