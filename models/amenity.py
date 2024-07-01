#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
import sqlalchemy
import os


class Amenity(BaseModel, Base):
    """ the class for the amentiy """
    __tablename__ = 'amenities'

    if os.environ.get('HBNB_TYPE_STORAGE') == 'db':
        name = Column(String(128), nullable=False)
    else:
        name = ""
