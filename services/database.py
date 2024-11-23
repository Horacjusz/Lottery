import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings.settings import DATABASE_URL
from models.models import Base

# Set up the database engine and session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
datasession = Session()

# Create tables
def initialize_db():
    Base.metadata.create_all(engine)
