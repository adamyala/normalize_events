from sqlalchemy.sql import select
from lib.category import Category
from lib.eventlog import EventLog
from lib.models import event


class Event(object):
    def __init__(self):
            self.address1 = None
            self.address2 = None
            self.api = None
            self.source = None
            self.city = None
            self.cost = None
            self.start_date = None
            self.end_date = None
            self.description = None
            self.link = None
            self.name = None
            self.place = None
            self.state = None
            self.zipcode = None
            self.event_id = None
            self.categories = None
            self.api_id = None

    def is_complete(self):
        requirements = [
            'name',
            'date',
            'place',
            'address1',
            'city',
            'state',
            'api',
            'link',
            'source',
        ]
        for requirement in requirements:
            try:
                if not getattr(self, requirement):
                    return EventLog(self.name, requirement, self.link, self.api)
            except AttributeError:
                return EventLog(self.name, requirement, self.link, self.api)
        return True

    def is_duplicate(self, connection):
        event_dupe = connection.execute(select([event.c.link]).where(
            event.c.link == self.link or event.c.name == self.name)
            ).rowcount
        return True if event_dupe > 0 else False

    def is_valid(self, connection):
        completeness = self.is_complete()
        if type(completeness) is EventLog:
            return completeness
        if self.is_duplicate(connection):
            return False
        return True

    def insert(self, connection):
        ins = event.insert().values(
            address1=self.address1,
            address2=self.address2,
            api=self.api,
            source=self.source,
            city=self.city,
            cost=self.cost,
            start_date=self.start_date,
            end_date=self.end_date,
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

    def set_categories(self, connection):
        event_category = Category(connection)
        event_category.get_categories_in_db()
        event_category.add_event_category(str(self.name) + ' ' + str(self.description), self.event_id)
        return self

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
