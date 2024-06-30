#!/usr/bin/python3
"""This module is a set of unit tests for Amenity"""
import unittest
import os
from models.engine.file_storage import FileStorage
from models.amenity import Amenity
from models import storageType


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
