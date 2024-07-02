#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base, storage_type
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """ the class for the amentiy """
    __tablename__ = 'amenities' # Defines the name of the table in the database

    # Conditional attribute definition based on storage type
    if storage_type == 'db':
        # Define the 'name' column in the table, with a max length of 128 characters, and cannot be null
        name = Column(String(128), nullable=False)
    else:
        # If storage is not database, set 'name' as an empty string
        name = ""
