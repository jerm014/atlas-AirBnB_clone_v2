#!/usr/bin/python3
"""This module is a set of unit tests for Amenity"""
import unittest
from models.amenity import Amenity
from models import storage_type


class TestAmenity(unittest.TestCase):
    """Class test for Amenity"""

    def setUp(self):
        """Set up test environment"""
        self.amenity = Amenity()

    def test_amenity_is_instance(self):
        """Test if Amenity instance is created"""
        self.assertIsInstance(self.amenity, Amenity)

    def test_amenity_has_name_attr(self):
        """Test if 'name' attribute exists in Amenity instance"""
        self.assertTrue(hasattr(self.amenity, 'name'))

    def test_amenity_name_initial_value(self):
        """Test initial value of 'name' attribute"""
        if storage_type == 'db':
            self.assertIsNone(self.amenity.name)
        else:
            self.assertEqual(self.amenity.name, "")

    def test_amenity_name_type(self):
        """Test type of 'name' attribute"""
        if storage_type == 'db':
            self.assertIsNone(self.amenity.name)
        else:
            self.assertIsInstance(self.amenity.name, str)
