from models import engine


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
        invalid = event.is_invalid(self.connection)
        if invalid is False:
            event.insert(self.connection)
            event.set_categories(self.connection)
        elif type(invalid) is not bool:
            invalid.insert(self.connection)
        return event.event_id

    def close_connection(self):
        self.connection.close()
        return True
