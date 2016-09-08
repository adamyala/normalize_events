import datetime
import json
from config import CLIENT_MU, CATEGORY
from lib.client import Client
from lib.event import Event
from lib.feeds import helpers


class MeetupClient(Client):
    def __init__(self, server, token):
        Client.__init__(self, server, token, 'Meetup')

    def get_json(self):
        return json.loads(self._get('/2/open_events', {
            'state': CLIENT_MU['state'],
            'category': CLIENT_MU['category'][CATEGORY],
            'status': 'upcoming',
            'key': self.token
            }).text)['results']

    def parse_events(self, events):
        result = []
        for event in events:
            if 'venue' not in event or 'state' not in event['venue'] or event['venue']['state'] != 'IL':
                continue
            try:
                curr_event = Event()
                curr_event.name = helpers.clean_string(event['name'])
                curr_event.description = helpers.clean_string(event['description'])
                curr_event.date = datetime.datetime.fromtimestamp(event['time']/1000)
                curr_event.place = event['venue']['name']
                curr_event.address1 = helpers.clean_address(event['venue']['address_1'])
                curr_event.address2 = None
                curr_event.city = helpers.clean_city(event['venue']['city'])
                curr_event.state = event['venue']['state']
                curr_event.zipcode = event['venue']['zip'] if 'zip' in event['venue'] else None
                if 'fee' in event and 'amount' in event['fee']:
                    curr_event.cost = event['fee']['amount']
                else:
                    curr_event.cost = 0
                curr_event.link = event['event_url']
                curr_event.api = 'https://api.meetup.com/2/events?key=' + self.token + '&event_id=' + event['id']
                curr_event.api_id = event['id']
                curr_event.source = self.source
                result.append(curr_event)
            except KeyError:
                self.logger.exception(
                    'meetup event parsing error',
                    event,
                    event['id']
                )
        return result

    def get_events(self):
        return self.parse_events(self.get_json())
