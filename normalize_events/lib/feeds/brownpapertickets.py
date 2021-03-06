import datetime
from bs4 import BeautifulSoup
from xml.etree import ElementTree
from config import CLIENT_BPT, CATEGORY
from lib.client import Client
from lib.event import Event
from lib.feeds import helpers


class BPTClient(Client):
    def __init__(self, server, token):
        Client.__init__(self, server, token, 'Brown Paper Tickets')

    def get_event_ids(self):
        page = 0
        result = []
        more_pages = True
        while more_pages:
            self.logger.debug('%s, parsing page %s', __name__, page)
            page += 1
            source = self._get('browse.html', {
                'start_date': datetime.date.today().strftime('%m/%d/%y'),
                'end_date': '12/31/2020',
                'category_id': CLIENT_BPT['category_id'][CATEGORY],
                'state': CLIENT_BPT['state'],
                'country': CLIENT_BPT['country'],
                'page': page
                })
            links = BeautifulSoup(source.text, "html.parser").findAll("a", "viewlink")
            self.logger.debug('%s, url: %s, links: %s', __name__, source.url, links)
            if links:
                group_ids = [str(link)[65:72] for link in links]
                for group_id in group_ids:
                    self.logger.debug('%s, group_id: %s', __name__, group_id)
                    result.append(self._get('group/{group_id}'.format(group_id=group_id)).url[39:])
            else:
                return self.parse_event_ids(result)

    def parse_event_ids(self, event_ids):
        db_ids = self.get_db_ids()
        result = []
        for event_id in event_ids:
            if event_id not in db_ids:
                result.append(event_id)
        return result

    def get_event_loc(self, event_id):
        response = self._get('api2/eventlist', {
            'event_id': event_id,
            'id': self.token
            })
        event = ElementTree.fromstring(response.text.encode('utf-8')).find('event')

        result = Event()
        result.name = helpers.clean_string(event.find('title').text)
        result.description = ' '.join([
            helpers.clean_string(event.find('description').text),
            helpers.clean_string(event.find('e_description').text)
        ])
        result.place = helpers.clean_address(event.find('e_address1').text)
        result.address1 = helpers.clean_address(event.find('e_address2').text)
        result.city = helpers.clean_city(event.find('e_city').text)
        result.state = event.find('e_state').text
        result.zipcode = event.find('e_zip').text
        result.link = event.find('link').text
        result.api = [response.url]
        result.source = 'Brown Paper Tickets'
        result.api_id = event_id
        return result

    def get_event_date(self, event_id):
        response = self._get('api2/datelist', {
            'event_id': event_id,
            'id': self.token
            })
        dates = ElementTree.fromstring(response.text.encode('utf-8')).findall('date')
        result = {
            'date': datetime.datetime.strptime('2050-01-01', '%Y-%m-%d'),
            'date_api': response.url
        }
        for date in dates:
            event_time = datetime.datetime.strptime(
                str(date.find('datestart').text) + 'T' + str(date.find('timestart').text),
                '%Y-%m-%dT%H:%M'
                )
            if event_time < result['date']:
                result['date'] = event_time
                result['date_id'] = date.find('date_id').text
        return result

    def get_event_cost(self, date_id):
        response = self._get('api2/pricelist', {
            'date_id': date_id,
            'id': self.token
            })
        prices = ElementTree.fromstring(response.text.encode('utf-8')).findall('price')
        event_cost = {
            'cost': 9999.00,
            'cost_api': response.url
        }
        for price in prices:
            event_price = float(price.find('value').text)
            if event_price < event_cost['cost']:
                event_cost['cost'] = event_price
        return event_cost

    def get_events(self):
        self.logger.info('%s, running get_events()', __name__)
        event_ids = self.get_event_ids()
        result = []
        for event_id in event_ids:
            event = self.get_event_loc(event_id)
            if event:
                event_date = self.get_event_date(event_id)
                event.date = event_date['date']
                event.api.append(event_date['date_api'])
                event_cost = self.get_event_cost(event_date['date_id'])
                event.cost = event_cost['cost']
                event.api.append(event_cost['cost_api'])
                result.append(event)
        self.logger.info('%s, finished get_events()', __name__)
        return result
