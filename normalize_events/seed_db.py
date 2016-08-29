from lib.category import Category
from config import CATEGORY
from lib.models import engine


with engine.connect() as connection:
    category = Category(connection)
    category.add_categories_to_db(category.category_objs[CATEGORY].categories)
