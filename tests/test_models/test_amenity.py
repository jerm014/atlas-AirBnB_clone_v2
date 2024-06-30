#!/usr/bin/python3
"""This module is a set of unit tests for Amenity"""
import unittest
import os
from models.engine.file_storage import FileStorage
from models.amenity import Amenity

my_model = Amenity()


class TestAmenity(unittest.TestCase):
    """Class test for Amenity"""

    def test_amenity(self):
        """Unit tests for Amenity"""
        amenity = Amenity()
        self.assertTrue(hasattr(amenity, 'name'))
        self.assertEqual(amenity.name, "")
