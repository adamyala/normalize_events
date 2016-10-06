import json
import time
from datetime import datetime
from dateutil import parser
from config import CLIENT_UNI, CATEGORY
from lib.client import Client
from lib.event import Event
from lib.feeds import helpers
from lib.maps import MapClient


class UniverseClient(Client):
    def __init__(self, server):
        Client.__init__(self, server, '', 'Universe')

    def get_page(self, offset=0):
        return json.loads(self._get('', {
            'query': CLIENT_UNI['category'][CATEGORY],
            'after': int(time.mktime(datetime.now().timetuple())),
            'latitude': 41.85069,
            'longitude': -87.65005,
            'limit': 50,
            'offset': offset,
            }).text)

    def parse_page(self, events_json):
        result = []
        map_client = MapClient()
        for event in events_json['discover_events']:
            if not event['address']:
                continue
            address_dict = map_client.breakdown_address(event['address'])
            if not address_dict:
                continue

            curr_event = Event()
            curr_event.name = helpers.clean_string(event['title'])
            curr_event.description = helpers.clean_string(event['description'])
            curr_event.start_date = parser.parse(event['start_time'])
            curr_event.end_date = parser.parse(event['end_time'])
            curr_event.place = event['location']
            curr_event.address1 = address_dict['address1']
            curr_event.address2 = None
            curr_event.city = address_dict['city']
            curr_event.state = address_dict['state']
            curr_event.zipcode = address_dict['zipcode']
            curr_event.cost = 0 if not event['price'] else event['price']
            curr_event.link = event['ticket_url']
            curr_event.api = 'https://www.universe.com/api/v2/event_id/' + str(event['id'])
            curr_event.source = self.source
            curr_event.api_id = event['id']
            result.append(curr_event)
        return result

    def get_events(self):
        self.logger.info('%s, running get_events()', __name__)
        first_page = self.get_page()
        total_events = int(first_page['meta']['count'])
        result = []
        events_done = 0
        result.extend(self.parse_page(first_page))
        events_done += 50
        while events_done < total_events:
            result.extend(self.parse_page(self.get_page(events_done)))
            events_done += 50
        self.logger.info('%s, finished get_events()', __name__)
        return result
