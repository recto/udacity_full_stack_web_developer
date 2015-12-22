import os
import sys
from settings import *
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    """ users table definition. """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    name = Column(String(250), nullable=False)
    picture = Column(String(250))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "picture": self.picture
        }


class Category(Base):
    """ categories table definition. """
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(1000))
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            "name": self.name,
            "description": self.description,
            "id": self.id,
            "user_id": self.user_id,
        }


class Item(Base):
    """ items table definition. """
    __tablename__ = "items"

    name = Column(String(250), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(1000))
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship(User)
    date = Column(DateTime, nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            "name": self.name,
            "description": self.description,
            "id": self.id,
            "category_id": self.category_id,
            "user_id": self.user_id,
        }


engine = create_engine("postgresql+psycopg2://%s:%s@%s:%d/%s" % (db_user, db_password, db_host, db_port, db_name))
Base.metadata.create_all(engine)
