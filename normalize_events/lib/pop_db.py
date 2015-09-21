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
            # print(curr_event.source + ', ' + curr_event.name)
            event.insert(self.connection)
            event.pick_categories(event.categories, self.connection)
        elif type(invalid) is not bool:
            invalid.insert(self.connection)
        return event.event_id

    def close_connection(self):
        self.connection.close()
        return True


    # gets events from each source
    # inserts them 1 by 1
    #      if maps are on, download maps

    # method to get all events
    # method to an insert event
    # method to download a map