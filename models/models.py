from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, JSON, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    visible = Column(Boolean, default=True)
    choosable = Column(Boolean, default=True)
    spouse = Column(Integer, ForeignKey('users.user_id'))
    assignment = Column(Integer)
    assigned_to = Column(Integer)
    admin = Column(Boolean, default=False)
    wishlist = Column(JSON, default=[])
    reserved_items = Column(JSON, default=[])


class Item(Base):
    __tablename__ = 'items'

    item_id = Column(Integer, primary_key=True)
    item_name = Column(String, nullable=False)
    item_description = Column(String, default="")
    reserved_by = Column(Integer, ForeignKey('users.user_id'))
    owner_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    bought = Column(Boolean, default=False)

class Setting(Base):
    __tablename__ = 'settings'

    key = Column(String, nullable=False)
    value = Column(JSON, nullable=False)
    __table_args__ = (PrimaryKeyConstraint('key', name='pk_settings'),)
