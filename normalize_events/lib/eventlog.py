from models import eventlog


class EventLog(object):
    def __init__(self, name, field, link, api):
        self.name = name
        self.field = field
        self.link = link
        self.api = api

    def insert(self, connection):
        ins = eventlog.insert().values(
            name=self.name,
            field=self.field,
            link=self.link,
            api=self.api,
            )
        return connection.execute(ins).inserted_primary_key[0]
