#!/usr/bin/python3
""" User Module for HBNB project """
from models.base_model import BaseModel, Base, storage_type
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """This class defines a user by various attributes"""
    __tablename__ = 'users'

    if storage_type == 'db':
        email = Column(String(128), nullable=False, default="")
        password = Column(String(128), nullable=False, default="")
        first_name = Column(String(128), nullable=True, default="")
        last_name = Column(String(128), nullable=True, default="")
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ''
        password = ''
        first_name = ''
        last_name = ''

    def __init__(self, *args, **kwargs):
        """Initializes user"""
        super().__init__(*args, **kwargs)
