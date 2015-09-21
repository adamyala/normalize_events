from ..client import Client
from ..event import Event
import json
import datetime
import helpers as h
from config import CLIENT_MU


class MeetupClient(Client):
    def __init__(self, server, token, source):
        Client.__init__(self, server, token, source)

    def get_json(self):
        return json.loads(self._get('/2/open_events', {
            'sign': 'true',
            'state': CLIENT_MU['state'],
            'category': CLIENT_MU['category'],
            'status': 'upcoming',
            'key': self.token
            }).text)['results']

    def parse_events(self, events):
        result = []
        for event in events:
            try:
                if event['venue']['state'] == 'IL':
                    curr_event = Event()
                    curr_event.source = 'Meetup'
                    curr_event.name = h.clean_string(event['name'])
                    curr_event.description = h.clean_string(event['description'])
                    curr_event.date = datetime.datetime.fromtimestamp(event['time']/1000)
                    curr_event.place = event['venue']['name']
                    curr_event.address1 = h.clean_address(event['venue']['address_1'])
                    curr_event.address2 = None
                    curr_event.city = h.clean_city(event['venue']['city'])
                    curr_event.state = event['venue']['state']
                    curr_event.zipcode = event['venue']['zip']
                    curr_event.cost = 0
                    curr_event.link = event['event_url']
                    curr_event.api = 'https://api.meetup.com/2/events?key=' + self.token + '&event_id=' + event['id']
                    curr_event.api_id = event['id']
                    curr_event.source = self.source
                    result.append(curr_event)
            except:
                pass
        return result

    def get_events(self):
        return self.parse_events(self.get_json())
