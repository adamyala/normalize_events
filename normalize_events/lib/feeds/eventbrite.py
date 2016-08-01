import datetime
import json
from config import CLIENT_EB, CATEGORY
from lib.client import Client
from lib.event import Event
from lib.feeds import helpers


class EventbriteClient(Client):
    def __init__(self, server, token):
        Client.__init__(self, server, token, 'Eventbrite')

    def get_event_ids(self):
        first_page = self.get_page()

        pages = 0
        try:
            pages = int(first_page['pagination']['page_count'])
        except KeyError:
            self.logger.exception('eventbrite auth error', first_page)

        event_ids = []
        event_ids.extend([event['id'] for event in first_page['events']])
        for page in range(2, pages + 1):
            event_ids.extend([event['id'] for event in self.get_page(page)['events']])
        db_ids = self.get_db_ids()
        result = []
        for event_id in event_ids:
            if event_id not in db_ids:
                result.append(event_id)
        return result

    def get_page(self, page=1):
        request = self._get('events/search/', {
            'page': page,
            'categories': CLIENT_EB['categories'][CATEGORY],
            'location.address': CLIENT_EB['location_address'],
            'location.within': CLIENT_EB['location_within'],
            'start_date.range_start': datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
            }, {'Authorization': 'Bearer ' + self.token})
        return json.loads(request.text)

    def get_event_detail(self, event_id):
        return json.loads(
            self._get(
                url='events/{event_id}/'.format(event_id=event_id),
                headers={'Authorization': 'Bearer ' + self.token}).text
            )

    def get_event_venue(self, venue_id):
        return json.loads(self._get(
            'venues/{venue_id}/'.format(venue_id=venue_id),
            None,
            {'Authorization': 'Bearer ' + self.token}
            ).text)

    def get_ticket_cost(self, ticket_id):
        ticket_prices = json.loads(self._get(
            '/events/{ticket_id}/ticket_classes/'.format(ticket_id=ticket_id),
            None,
            {'Authorization': 'Bearer ' + self.token}
            ).text)['ticket_classes']
        cost = 0
        for ticket_price in ticket_prices:
            if ticket_price['free'] or ticket_price['donation']:
                return cost
            new_cost = (ticket_price['cost']['value'] + ticket_price['fee']['value'])/100
            if new_cost < cost or cost is 0:
                cost = new_cost
        return cost

    def build_event(self, event_id):
        # Eventbrite limits API calls severely, so we check to see if we already have
        # the event in the database before wasting API calls
        curr_event = Event()
        event_detail = self.get_event_detail(event_id)
        curr_event.link = event_detail['url']
        if curr_event.is_duplicate(self.connection):
            return False

        try:
            curr_event.name = helpers.clean_string(event_detail['name']['text'])
            curr_event.date = datetime.datetime.strptime(event_detail['start']['local'], '%Y-%m-%dT%H:%M:%S')
            curr_event.description = helpers.clean_string(event_detail['description']['text'])
            curr_event.api = event_detail['resource_uri'] + '?token=' + self.token
            curr_venue = self.get_event_venue(event_detail['venue_id'])
            curr_event.place = helpers.clean_address(curr_venue['name'])
            curr_event.address1 = helpers.clean_address(curr_venue['address']['address_1'])
            curr_event.address2 = helpers.clean_address(curr_venue['address']['address_2'])
            curr_event.city = helpers.clean_city(curr_venue['address']['city'])
            curr_event.state = curr_venue['address']['region']
            curr_event.zipcode = curr_venue['address']['postal_code']
            curr_event.cost = self.get_ticket_cost(event_detail['id'])
            curr_event.source = self.source
            curr_event.api_id = event_detail['id']

            # We also do inserts here because the API can give us API limit errors at anytime.
            # The is_valid check later will not insert dupes.
            valid = curr_event.is_valid(self.connection)
            if valid is True:
                curr_event.insert(self.connection)
                curr_event.set_categories(self.connection)
            elif type(valid) is not bool:
                valid.insert(self.connection)

            return curr_event
        except KeyError:
            # TODO: Add real exception handling or remove this
            self.logger.exception(
                'eventbrite event parsing error',
                event_detail,
                event_detail['id']
            )

    def get_events(self):
        self.logger.info('%s, running get_events()', __name__)
        event_ids = self.get_event_ids()
        result = []
        for event_id in event_ids:
            curr_event = self.build_event(event_id)
            if curr_event:
                result.append(curr_event)
        self.logger.info('%s, finished get_events()', __name__)
        return result
