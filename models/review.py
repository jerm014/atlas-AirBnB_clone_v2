#!/usr/bin/python3
""" Review module for the HBNB project """
from models.base_model import BaseModel, Base, storage_type
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship


class Review(BaseModel, Base):
    """ Review class to store review information """
    __tablename__ = 'reviews' # Defines the name of the table in the database

    # Conditional attribute definition based on storage type
    if storage_type == 'db':
        # Define the 'place_id' column in the table, referencing 'id' column
        # of 'places' table, cannot be null
        place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
        # Define the 'user_id' column in the table, referencing 'id' column
        # and cannot be null
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        # Define the 'text' column in the table, with a max length of 1024 characters,
        # and cannot be null
        text = Column(String(1024), nullable=False)
    else:
        # If storage is not database, set 'place_id', 'user_id', and 'text' as empty strings
        place_id = ""
        user_id = ""
        text = ""
