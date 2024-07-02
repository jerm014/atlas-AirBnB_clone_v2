#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_BaseModel
from models.state import State
from models import storage_type


class test_State(test_BaseModel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "State"
        self.value = State

    def test_name3(self):
        """ """
        pass
        #  new = self.value()
        #  self.assertEqual(type(new.name), str)
