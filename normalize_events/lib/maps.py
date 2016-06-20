from lib.client import Client
import os
import shutil
import requests


class MapClient(Client):
    def __init__(self, server, token):
        Client.__init__(self, server, token)

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
        components = requests.get(
            url='https://maps.googleapis.com/maps/api/geocode/json',
            params={'address': address_string}
        ).json()['results'][0]['address_components']
        address_dict = {x['types'][0]: x['short_name'] for x in components}
        return {
            'address1': address_dict['street_number'] + ' ' + address_dict['route'],
            'city': address_dict['locality'],
            'state': address_dict['administrative_area_level_1'],
            'zipcode': address_dict['postal_code'],
        }