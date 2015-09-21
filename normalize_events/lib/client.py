import requests
from models import *
from sqlalchemy.sql import select

class Client(object):
    def __init__(self, server, token, source=None):
        self.token = token
        self.server = server
        self.connection = engine.connect()
        self.source = source

    def _get(self, url, params=None, headers=None, stream=False):
        return requests.get(
            '{server}/{url}'.format(server=self.server, url=url),
            params=params,
            headers=headers,
            stream=stream,
            )

    def get_db_ids(self):
        db_proxy = self.connection.execute(
            select([event.c.api_id]).where(event.c.source == self.source)
            )
        return [row['api_id'].encode('utf-8') for row in db_proxy.fetchall()]
