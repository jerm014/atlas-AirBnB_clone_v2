#!/usr/bin/python3
""" User Module for HBNB project """
from models.base_model import BaseModel, Base, storage_type
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """This class defines a user by various attributes"""
    __tablename__ = 'users' # Defines the table name in the database

    if storage_type == 'db':
        # Define 'email' column, max length 128 characters, cannot be null
        email = Column(String(128), nullable=False, default="")
        # Define 'password' column, max length 128 characters, cannot be null
        password = Column(String(128), nullable=False, default="")
        # Define 'first_name' column, max length 128 characters, can be null
        first_name = Column(String(128), nullable=True, default="")
        # Define 'last_name' column, max length 128 characters, can be nul
        last_name = Column(String(128), nullable=True, default="")
        # User has many places, each place has a back reference to user
        places = relationship("Place", backref="user")
        # User has many reviews, each review has a back reference to user
        reviews = relationship("Review", backref="user")
    else:
        # If storage is not a database, set attributes to empty strings
        email = ''
        password = ''
        first_name = ''
        last_name = ''

    def __init__(self, *args, **kwargs):
        """Initializes user"""
        super().__init__(*args, **kwargs) # Calls the super class init method
