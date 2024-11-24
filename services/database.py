import psycopg2 # Required for pipreqs
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,scoped_session
from settings.settings import DATABASE_URL
from models.models import Base

engine = create_engine(DATABASE_URL)
session_factory = sessionmaker(bind = engine)
datasession = scoped_session(session_factory)

def initialize_db():
    Base.metadata.create_all(engine)
