from lib.client import Client
import os
import shutil


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
