import psycopg2 # Required for pipreqs
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,scoped_session
from settings.settings import DATABASE_URL
from models.models import Base

# engine = create_engine(DATABASE_URL)
engine = create_engine("postgresql://lottery_db_user:UmwThpbF9qsTWZYLW4mIE4v304FuwHz9@dpg-ct0vom1u0jms73caihf0-a.frankfurt-postgres.render.com/lottery_db")
session_factory = sessionmaker(bind = engine)
datasession = scoped_session(session_factory)

def initialize_db():
    Base.metadata.create_all(engine)
