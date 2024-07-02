#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base, storage_type
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    __tablename__ = 'cities' # Defines the name of the table in the database

    # Conditional attribute definition based on storage type
    if storage_type == 'db':
        # Define the 'state_id' column in the table, referencing 'id' column of 'states' table, cannot be null
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        # Define the 'name' column in the table, with a max length of 128 characters, and cannot be null
        name = Column(String(128), nullable=False)
         # Relationship definition: City has many places, each place has a back reference to cities
        places = relationship("Place", backref="cities")
    else:
        # If storage is not database, set 'name' and 'state_id' as empty strings
        name = ""
        state_id = ""
