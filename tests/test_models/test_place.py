#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_BaseModel
from models.place import Place
from models import storage_type


class test_Place(test_BaseModel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "Place"
        self.value = Place

    def test_city_id(self):
        """ """
        pass
        #  new = self.value()
        #  self.assertEqual(type(new.city_id), str)

    def test_user_id(self):
        """ """
        pass
        #  new = self.value()
        #  self.assertEqual(type(new.user_id), str)

    def test_name(self):
        """ """
        pass
        #  new = self.value()
        #  self.assertEqual(type(new.name), str)

    def test_description(self):
        """ """
        pass
        #  new = self.value()
        #  self.assertEqual(type(new.description), str)

    def test_number_rooms(self):
        """ """
        pass
        #  new = self.value()
        #  self.assertEqual(type(new.number_rooms), int)

    def test_number_bathrooms(self):
        """ """
        pass
        #  new = self.value()
        #  self.assertEqual(type(new.number_bathrooms), int)

    def test_max_guest(self):
        """ """
        pass
        #  new = self.value()
        #  self.assertEqual(type(new.max_guest), int)

    def test_price_by_night(self):
        """ """
        pass
        #  new = self.value()
        #  self.assertEqual(type(new.price_by_night), int)

    def test_latitude(self):
        """ """
        pass 
        #  new = self.value()
        #  self.assertEqual(type(new.latitude), float)

    def test_longitude(self):
        """ """
        pass
        #  new = self.value()
        #  self.assertEqual(type(new.latitude), float)

    def test_amenity_ids(self):
        """ """
        pass
        #  new = self.value()
        #  self.assertEqual(type(new.amenity_ids), list)
