from eventlog import EventLog
from models import event, eventcategory
from sqlalchemy.sql import select


class Event(object):
    def __init__(self):
            self.address1 = None
            self.address2 = None
            self.api = None
            self.source = None
            self.city = None
            self.cost = None
            self.date = None
            self.description = None
            self.link = None
            self.name = None
            self.place = None
            self.state = None
            self.zipcode = None
            self.event_id = None
            self.categories = None

    def is_incomplete(self):
        requirements = [
            'name', 'description', 'date',
            'place', 'address1', 'city',
            'state', 'cost', 'api',
            'link', 'source'
            ]
        for requirement in requirements:
            try:
                getattr(self, requirement)
            except:
                return EventLog(self.name, requirement, self.link, self.api)
        return False

    def is_duplicate(self, connection):
        event_dupe = connection.execute(select([event.c.link]).where(
            event.c.link == self.link or event.c.name == self.name)
            ).rowcount
        return True if event_dupe > 0 else False

    def is_invalid(self, connection):
        completeness = self.is_incomplete()
        if type(completeness) is bool:
            return completeness or self.is_duplicate(connection)
        else:
            return completeness

    def insert(self, connection):
        ins = event.insert().values(
            address1=self.address1,
            address2=self.address2,
            api=self.api,
            source=self.source,
            city=self.city,
            cost=self.cost,
            date=self.date,
            description=self.description,
            link=self.link,
            name=self.name,
            place=self.place,
            state=self.state,
            zipcode=self.zipcode,
            api_id=self.api_id,
            )
        self.event_id = connection.execute(ins).inserted_primary_key[0]
        return self.event_id

    def old_code(self, connection):
        event_string = self.name + self.description
        other = True
        self.category_algo(event_string)
        for curr_category in self.categories:
            ins = eventcategory.insert().values(event_id=self.event_id, category_id=curr_category['id'])
            connection.execute(ins)
            other = False
        if other:
            ins = eventcategory.insert().values(event_id=self.event_id, category_id=12)
            connection.execute(ins)
        return self

    def set_categories(self):
        event_string = self.name + self.description
        self.categories = self.category_algo(event_string)
        return self

    def category_algo(self, event_string):
        result = []
        return result

    def get_address(self):
        result = ""
        if self.address1:
            result = self.address1 + ' '
        if self.city:
            result = result + self.city + ' '
        if self.state:
            result = result + self.state + ' '
        if self.zipcode:
            result = result + self.zipcode
        return result
