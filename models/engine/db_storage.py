#!/usr/bin/python3
""" MySQL Database Storage """

import models
from models.base_model import BaseModel, Base
from models import User, State, City, Amenity, Place, Review
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

__engine = None
__session = None

classes = {"Amenity": Amenity,
           "City": City,
           "Place": Place,
           "Review": Review,
           "State": State,
           "User": User}

""" Initialize the MySQL Database Storage """

username = getenv('HBNB_MYSQL_USER')
password = getenv('HBNB_MYSQL_PWD')
host = getenv('HBNB_MYSQL_HOST')
db_name = getenv('HBNB_MYSQL_DB')
connection = f'mysql+mysqldb://{username}:{password}@{host}/{db_name}'


class DBStorage:
    """MySQL database via sqlalchemy"""
    __engine = None
    __session = None

    def __init__(self):
        """make a DBStorage object and connect to the database"""
        self.__engine = create_engine(connection)

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls == clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        print(f"new dict is {new_dict}")
        return (new_dict)

    def new(self, obj):
        """ Add an object to the session """
        self.__session.add(obj)

    def save(self):
        """ Commit changes to database """
        self.__session.commit()

    def delete(self, obj=None):
        """ Delete an object from the current session """
        if obj is None:
            return
        self.__session.delete(obj)

    def reload(self):
        """ Create all tables in the database """

        Base.metadata.create_all(self.__engine)
        # Create a new session using sessionmaker
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)

        # Use scoped_session to ensure thread-safety
        self.__session = scoped_session(Session)()
