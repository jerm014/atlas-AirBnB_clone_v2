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
            HBNBCommand().onecmd(
                'create User first_name="John" last_name="Doe" password="Hunter2"'
                )
            instance_id = output.getvalue().strip()
            self.assertTrue(len(instance_id) > 0)
            # Clear the buffer
            output.truncate(0)
            output.seek(0)
            # Verify that the instance has been created with correct attributes
            HBNBCommand().onecmd(f'show User {instance_id}')
            instance_output = output.getvalue().strip()
            self.assertIn("John", instance_output)
            self.assertIn("Doe", instance_output)
            self.assertIn("Hunter2", instance_output)

    def test_create_with_invalid_class(self):
        """Test creating a new instance with an invalid class"""
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd(
                'create InvalidClass name="John Doe"'
                )
            self.assertEqual(output.getvalue().strip(),
                             "** class 'InvalidClass' doesn't exist**")

    def test_create_with_missing_class_name(self):
        """Test creating a new instance without specifying class name"""
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd('create')
            self.assertEqual(output.getvalue().strip(),
                             "** class name missing **"
                             )

    def test_create_with_invalid_params(self):
        """Test creating a new instance with invalid parameters"""
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd('create User name=John Doe age=thirty')
            self.assertIn(
                "** Invalid parameter value **", output.getvalue().strip()
                )


if __name__ == "__main__":
    unittest.main()
