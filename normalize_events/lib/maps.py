import os
import shutil
import requests
from config import CLIENT_GM
from lib.client import Client


class MapClient(Client):
    def __init__(self):
        Client.__init__(self, CLIENT_GM['url'], CLIENT_GM['token'])

    def download_map(self, address, event_id):
        request = self._get('maps/api/staticmap', {
            'size': '250x150',
            'center': address,
            'zoom': 15,
            'markers': 'size:small|color:red|label:1|' + address,
            'key': self.token,
            }, stream=True)

        if request.status_code == 200:
            with open(os.path.dirname(os.path.realpath(__file__)) + '/../../maps/' + str(event_id) + '.png', 'wb') as f:
                request.raw.decode_content = True
                shutil.copyfileobj(request.raw, f)
            return True
        else:
            return False

    def breakdown_address(self, address_string):
        results = requests.get(
            url='https://maps.googleapis.com/maps/api/geocode/json',
            params={'address': address_string}
        ).json()['results']

        if not results:
            return False

        components = results[0]['address_components']
        address_dict = {x['types'][0]: x['short_name'] for x in components}

        if not all(key in address_dict for key in (
            'locality', 'administrative_area_level_1', 'postal_code'
        )):
            return False

        return {
            'address1': ' '.join([
                address_dict.get('street_number', ''), address_dict.get('route', '')
            ]),
            'city': address_dict['locality'],
            'state': address_dict['administrative_area_level_1'],
            'zipcode': address_dict['postal_code'],
        }