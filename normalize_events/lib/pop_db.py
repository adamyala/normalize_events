from lib.models import engine


class PopDb(object):
    def __init__(self, clients):
        self.connection = engine.connect()
        self.clients = clients
        self.events = []

    def set_events(self):
        for client in self.clients:
            self.events.extend(client.get_events())
        return self

    def insert_event(self, event):
        valid = event.is_valid(self.connection)
        if valid is True:
            event.insert(self.connection)
            event.set_categories(self.connection)
        elif type(valid) is not bool:
            valid.insert(self.connection)
        return event.event_id

    def close_connection(self):
        self.connection.close()
        return True
