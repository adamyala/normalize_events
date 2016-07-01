import datetime
import json
from config import CATEGORY, CLIENT_EF
from lib.client import Client
from lib.event import Event
from lib.feeds import helpers


class EventfulClient(Client):
    def __init__(self, server, token):
        Client.__init__(self, server, token, 'Eventful')

    def get_page(self, page_number=1):
        return json.loads(self._get('search/', {
            'app_key': self.token,
            'category': CLIENT_EF['category'][CATEGORY],
            'location': CLIENT_EF['location'],
            'date': 'Future',
            'page_size': 10,
            'include': 'price,categories',
            'page_number': page_number
            }).text)

    def parse_page(self, events_json):
        result = []
        for event in events_json['events']['event']:
            curr_event = Event()
            curr_event.name = helpers.clean_string(event['title'])
            curr_event.description = helpers.clean_string(event['description'])
            curr_event.date = datetime.datetime.strptime(event['start_time'], "%Y-%m-%d %H:%M:%S")
            curr_event.place = event['venue_name']
            curr_event.address1 = helpers.clean_address(event['venue_address'])
            curr_event.address2 = None
            curr_event.city = helpers.clean_city(event['city_name'])
            curr_event.state = event['region_abbr']
            curr_event.zipcode = event['postal_code']
            curr_event.cost = 0 if 'cost' not in event else event['cost']
            curr_event.link = event['url']
            curr_event.api = 'http://api.eventful.com/rest/events/get?app_key=' + self.token + '&id=' + event['id']
            curr_event.source = self.source
            curr_event.api_id = event['id']
            result.append(curr_event)
        return result

    def get_events(self):
        first_page = self.get_page()
        pages = int(first_page['page_count'])
        result = []
        result.extend(self.parse_page(first_page))
        for page in range(2, pages + 1):
            result.extend(self.parse_page(self.get_page(page)))
        return result
