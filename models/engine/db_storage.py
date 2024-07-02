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
        """ returns a dictionary of some things or all things """
        all_dict = {}
        if cls:
            if isinstance(cls, str):
                cls = eval(cls)
            query = self.__session.query(cls)
            for elem in query:
                key = "{}.{}".format(type(elem).__name__, elem.id)
                # del elem.__dict__["_sa_instance_state"]
                all_dict[key] = elem
        else:
            for clases in [State, City, User, Place, Review, Amenity]:
                query = self.__session.query(clases)
                for elem in query:
                    key = "{}.{}".format(type(elem).__name__, elem.id)
                    # del elem.__dict__["_sa_instance_state"]
                    all_dict[key] = elem
        return (all_dict)

    def new(self, obj):
        """ Add an object to the session """
        self.__session.add(obj)

    def save(self):
        """ Commit changes to database """
        self.__session.commit()

    def delete(self, key=None):
        """ Delete an object from the current session """
        split_key = key.split(".")
        class_name = split_key[0]
        obj_id = split_key[1]
        obj = {}
        if class_name not in classes:
            return
        for o in self.all(class_name).items():
            if o[1].id == obj_id:
                obj = o[1]
                break
        if obj is None:
            print(" ** object not found to delete ** ")
            return
        self.__session.delete(obj)
        print(f"Deleted {key}")

    def reload(self):
        """ Create all tables in the database """

        Base.metadata.create_all(self.__engine)
        # Create a new session using sessionmaker
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)

        # Use scoped_session to ensure thread-safety
        self.__session = scoped_session(Session)()

    def add_amenity(self, place_id, amenity_id):
        """ Add an amenity to a place """
        place = self.__session.query(Place).get(place_id)
        amenity = self.__session.query(Amenity).get(amenity_id)
        if place and amenity:
            place.amenities.append(amenity)
            self.__session.commit()
