#!/usr/bin/python3
""" MySQL Database Storage """

import models
from models.base_model import BaseModel, Base
from models import User, State, City, Amenity, Place, Review
from os import getenv
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker

#  Initialize the MySQL Database Storage
username = getenv('HBNB_MYSQL_USER')
password = getenv('HBNB_MYSQL_PWD')
host = getenv('HBNB_MYSQL_HOST')
db_name = getenv('HBNB_MYSQL_DB')
connection = f'mysql+mysqldb://{username}:{password}@{host}/{db_name}'

#  username = "hbnb_dev"
#  password = "hbnb_dev_pwd"
#  host = "localhost"
#  db_name = "hbnb_dev_db"
#  connection = f'mysql+mysqldb://{username}:{password}@{host}/{db_name}'


class DBStorage:
    """MySQL database via sqlalchemy"""
    __engine = create_engine(connection)
    __session = None

    classes = {"Amenity": Amenity,
               "City": City,
               "Place": Place,
               "Review": Review,
               "State": State,
               "User": User}

    def __init__(self):
        """make a DBStorage object and connect to the database"""
        pass

    def all(self, cls=None):
        """Query all objects in the current database session"""
        objs = {}
        if cls:
            #  support searching for a specific class by Class or 'Class'
            if isinstance(cls, str):
                if cls in self.classes:
                    cls = self.classes[cls]
                else:
                    #  user didn't provide a class we can use
                    #  call us again without a cls specifier
                    return (self.all())
            #  If valid class specified, query all objects of that class
            results = self.__session.query(cls).all()
            for obj in results:
                key = f"{cls.__name__}.{obj.id}"
                objs[key] = obj
        else:
            # If no class specified, query objects of all classes
            classes = [User, State, City, Amenity, Place, Review]
            for class_ in classes:
                results = self.__session.query(class_).all()
                for obj in results:
                    key = f"{class_.__name__}.{obj.id}"
                    objs[key] = obj
        return objs

    def new(self, obj):
        """ Add an object to the session """
        # add the obj to the __session if it isn't already there
        if obj not in self.__session:
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
        """Create all tables in database"""

        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def link_amenity(self, amenity_id, place_id):
        """ Add an amenity to a place """
        place = amenity = None
        place = self.all('Place')['Place.' + place_id]
        amenity = self.all('Amenity')['Amenity.' + amenity_id]

        if place is None:
            print(" ** Place not found ** ")
            return False
        if amenity is None:
            print(" ** Amenity not found ** ")
            return False

        if place and amenity:
            place.amenities.append(amenity)
            self.__session.add(place)
            try:
                self.__session.commit()
                print(" ** Amenity and Place linked ** ")
                return True
            except exc.IntegrityError as e:
                if 'Duplicate entry' in str(e.orig):
                    print(" ** Amenity and Place already linked ** ")
                else:
                    print(e)
                self.__session.rollback()
                return False
            except Exception as e:
                print(e)
                self.__session.rollback()
                return False

    def unlink_amenity(self, amenity_id, place_id):
        """ Remove an amenity from a place """
        place = amenity = None
        place = self.all('Place')['Place.' + place_id]
        amenity = self.all('Amenity')['Amenity.' + amenity_id]

        if place is None:
            print(" ** Place not found ** ")
            return False
        if amenity is None:
            print(" ** Amenity not found ** ")
            return False

        if place and amenity:
            if amenity in place.amenities:
                place.amenities.remove(amenity)
                self.__session.add(place)
                try:
                    self.__session.commit()
                    print(" ** Amenity and Place unlinked ** ")
                    return True
                # Handle MySQLdb._exceptions.IntegrityError here

                except self.__engine._exceptions.IntegrityError as e:
                    print(e[1])
                    self.__session.rollback()
                    return False
                except Exception as e:
                    print(e)
                    self.__session.rollback()
                    return False
            else:
                print(" ** Amenity and Place not linked ** ")
                return False

    def close(self):
        self.__session.remove()
