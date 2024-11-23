import psycopg2 # Required for pipreqs
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings.settings import DATABASE_URL
from models.models import Base

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
datasession = Session()

def initialize_db():
    Base.metadata.create_all(engine)
