from sqlalchemy.sql import select
from config import CATEGORY
from lib.models import eventcategory, category
from lib.category_lib import food, music


class Category(object):
    def __init__(self, connection):
            self.connection = connection
            self.category_objs = {
                'Food': food.Food(),
                'Music': music.Music(),
            }
            self.categories_in_db = []

    def get_categories_in_db(self):
        query = select([category.c.category])
        self.categories_in_db = self.connection.execute(query).fetchall()
        return self

    def add_categories_to_db(self, event_categories):
        self.get_categories_in_db()
        for category_type in event_categories:
            if category_type not in self.categories_in_db:
                category.insert().values(category=category_type)
        self.get_categories_in_db()
        return self

    def add_category_to_db(self, category_string):
        ins = category.insert().values(category=category_string)
        return self.connection.execute(ins).inserted_primary_key[0]

    def add_event_category(self, event_string, event_id):
        event_categories = self.category_objs[CATEGORY].get_categories_for_insert(event_string)
        for event_category in event_categories:
            if event_category in self.categories_in_db:
                ins = eventcategory.insert().values(
                    event_id=event_id,
                    category_id=self.categories_in_db[event_category]
                )
                self.connection.execute(ins)
            else:
                category_id = self.add_category_to_db(event_category)
                ins = eventcategory.insert().values(event_id=event_id, category_id=category_id)
                self.connection.execute(ins)

        return self
