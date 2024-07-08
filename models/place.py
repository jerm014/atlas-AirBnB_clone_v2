#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base, storage_type
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from models import Amenity, City


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'

    if storage_type == 'db':
        city_id = Column(String(60),
                         ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60),
                         ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship("Review", backref="place")
        place_amenity = Table('place_amenity', Base.metadata,
                              Column('place_id', String(60),
                                     ForeignKey('places.id',
                                                onupdate='CASCADE',
                                                ondelete='CASCADE'),
                                     primary_key=True,
                                     nullable=False),
                              Column('amenity_id', String(60),
                                     ForeignKey('amenities.id',
                                                onupdate='CASCADE',
                                                ondelete='CASCADE'),
                                     primary_key=True,
                                     nullable=False))
        amenities = relationship("Amenity",
                                 secondary="place_amenity",
                                 backref="place_amenities",
                                 viewonly=False)

    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []
        review_ids = []
        amenities = []
        reviews = []

        @property
        def reviews(self):
            """return a list of reviews"""
            from models.review import Review
            review_list = []
            all_reviews = models.storage.all(Review)
            for review in all_reviews.values():
                if str(review.place_id) == str(self.id):
                    review_list.append(review)
            return review_list

        @property
        def amenities(self):
            """Get/set linked Amenities."""
            amenity_list = []
            for amenity in list(storage.all("Amenity").values()):
                if amenity.id in self.amenity_ids:
                    amenity_list.append(amenity)
            return amenity_list

        @amenities.setter
        def amenities(self, value):
            if isinstance(value, Amenity):
                self.amenity_ids.append(value.id)

        @property
        def cities(self):
            """Get/set linked Cities."""
            city_list = []
            for city in list(storage.all("City").values()):
                if city.id == self.city_id:
                    city_list.append(city)
            return city_list

        @cities.setter
        def cities(self, value):
            if isinstance(value, City):
                self.city_id = value.id
