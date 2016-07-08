import json
import logging.config
import requests
from sqlalchemy.sql import select
from lib.models import engine, event


class Client(object):
    def __init__(self, server, token, source=None, log_config_path='logging.json'):
        self.token = token
        self.server = server
        self.connection = engine.connect()
        self.source = source
        self.logger = self.setup_logging(log_config_path)

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

    def setup_logging(self, log_config_path):
        with open(log_config_path, 'rt') as log_config_file:
            config_json = json.load(log_config_file)
        logging.config.dictConfig(config_json)
        return logging.getLogger(__name__)
