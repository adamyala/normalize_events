from normalize_events import config
from sqlalchemy import create_engine, func, Column, Table, MetaData
from sqlalchemy import Integer, String, DateTime, Numeric
from sqlalchemy.engine.url import URL

engine = create_engine(URL(**config.DATABASE))
metadata = MetaData()

event = Table(
    'event',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('created', DateTime, default=func.now()),
    Column('name', String),
    Column('description', String),
    Column('date', DateTime),
    Column('place', String),
    Column('address1', String),
    Column('address2', String),
    Column('city', String),
    Column('state', String),
    Column('zipcode', String),
    Column('cost', Numeric),
    Column('link', String),
    Column('api', String),
    Column('source', String),
    Column('api_id', String)
)

category = Table(
    'category',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('category', String)
)

eventcategory = Table(
    'eventcategory',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('event_id', Integer),
    Column('category_id', Integer)
    )

eventlog = Table(
    'eventlog',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('created', DateTime, default=func.now()),
    Column('name', String),
    Column('field', String),
    Column('link', String),
    Column('api', String)
    )

metadata.create_all(engine)
