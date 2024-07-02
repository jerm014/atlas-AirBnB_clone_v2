#!/usr/bin/python3
"""Defines the FileStorage class."""
import json


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
