#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base, storage_type
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """ the class for the amentiy """
    __tablename__ = 'amenities'

    if storage_type == 'db':
        name = Column(String(128), nullable=False)
    else:
        name = ""
