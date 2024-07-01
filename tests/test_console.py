#!/usr/bin/python3
import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand


class TestHBNBCommand(unittest.TestCase):
    """Unit tests for HBNBCommand class"""

    def test_create_with_valid_params(self):
        """Test creating a new instance with valid parameters"""
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd('create User name="John Doe" age=30 height=1.75')
            instance_id = output.getvalue().strip()
            self.assertTrue(len(instance_id) > 0)
            # Clear the buffer
            output.truncate(0)
            output.seek(0)
            # Verify that the instance has been created with correct attributes
            HBNBCommand().onecmd(f'show User {instance_id}')
            instance_output = output.getvalue().strip()
            self.assertIn("John Doe", instance_output)
            self.assertIn("age: 30", instance_output)
            self.assertIn("height: 1.75", instance_output)

