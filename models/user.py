#!/usr/bin/python3
""" User Module for HBNB project """
from models.base_model import BaseModel, Base
import sqlalchemy
import os


class User(BaseModel, Base):
    """This class defines a user by various attributes"""
    __tablename__ = 'users'

    if os.environ.get('HBNB_TYPE_STORAGE') == 'db':
        name = Column(String(128), nullable=False)
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
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
