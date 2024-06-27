#!/usr/bin/python3
""" MySQL Database Storage """

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model_state import Base
from os import getenv
from models.amenity import Amenity
from django.contrib.auth.models import User
__engine = None
__session = None


def __init__(self):
    """ Initialize the MySQL Database Storage """

    username = getenv('HBNB_MYSQL_USER')
    password = getenv('HBNB_MYSQL_PWD')
    host = getenv('HBNB_MYSQL_HOST')
    db_name = getenv('HBNB_MYSQL_DB')
    connection = f'mysql+mysqldb://{username}:{password}@{host}/{db_name}'

    self.__engine = create_engine(connetion, pool_pre_ping=True)
    Session = sessionmaker(bind=self.__engine)
    self.__session = Session()

def all(self, cls=None):
    """ Query on the current database session """
    new_dict = {}

    if cls = None:
        states = self.__session.query(State).all()
        citys = self.__session.query(City).all()
        users = self.__session.query(User).all()
        places = self.__session.query(Place).all()
        amenitys = self.__session.query(Amenity).all()
        reviews = self.__session.query(Review).all()
        self.reload()
        return users + states + citys + amenitys + places + reviews

    for obj in self.__session.query(cls).all():
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        new_dict[key] = obj
        return new_dict

def new(self, obj):
    """ Add the object to the current database session """
    self.__session.add(obj)

def save(self):
    """ Commit all changes of the current database session """
    self.__session.commit()

def delete(self, obj=None):
    """ Delete from the current database session """
    if obj is None:
        return
    self.__session.delete(obj)

def reload(self):
    """ Create all tables in the database """
    from models import user, state, city, amenity, place, review

    Base.metadata.create_all(self.__engine) 
    # Create a new session using sessionmaker
    Session = sessionmaker(bind=self.__engine, expire_on_commit=False)

    # Use scoped_session to ensure thread-safety
    self.__session = scoped_session(Session)()
