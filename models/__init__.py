#!/usr/bin/python3
from os import getenv
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.user import User

if getenv('HBNB_TYPE_STORAGE') == 'db':
    print("using db storage")
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    print("using file storage")
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()
