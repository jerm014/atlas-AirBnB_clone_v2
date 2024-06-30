#!/usr/bin/python3
import os

if os.environ.get('HBNB_TYPE_STORAGE') == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
    storageType = "db"
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
    storageType = "file"

storage.reload()
