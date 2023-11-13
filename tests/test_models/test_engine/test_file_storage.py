#!/usr/bin/python3
"""Test module to test the file_storage module
Created by:
    Samuel Ezeh
    Emmanuel Ochoja
"""

from models.base_model import BaseModel
from models.engine import file_storage
from models.engine.file_storage import FileStorage
import inspect
import json
import os
import unittest


class TestFileStorage(unittest.TestCase):
    """Tests the FileStorage class methods and attributes
    """
    def setUp(self):
        self.base = BaseModel()
        self.storage = FileStorage()
        self.file_path = "file.json"
        self.test_file = "test_file.json"
        self.storage.new(self.base)
        self.functions = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_module_documentation(self):
        """tests that module is documented
        """
        self.assertGreater(len(file_storage.__doc__), 1)

    def test_class_documentation(self):
        """tests that the class is documented
        """
        self.assertGreater(len(FileStorage.__doc__), 1)

    def test_function_documentation(self):
        """tests that the functions are documented
        """
        for name, function in self.functions:
            self.assertGreater(len(function.__doc__), 1)

    def test_all(self):
        """tests that all() is a dict and made up of instances
        """
        self.assertIsInstance(self.storage.all(), dict)
        self.assertTrue(len(self.storage.all()) > 0)

    def test_new(self):
        """tests that new() add an object to the objects dictionary
        """
        key = "{}.{}".format(self.base.__class__.__name__,
                             self.base.id)
        self.assertIn(key, self.storage.all())

    def test_save(self):
        """tests that save creates a new file
        """
        self.storage.save()
        self.assertTrue(os.path.exists(self.file_path))

    def test_save_overwrites_existing_file(self):
        """tests that save overwrites the file path if exists
        """
        time_1 = os.path.getmtime(self.file_path)
        self.storage.save()
        time_2 = os.path.getmtime(self.file_path)
        self.assertGreater(time_2, time_1)

    def test_that_save_writes_data(self):
        """tests that save writes the right data to file
        """
        key = "{}.{}".format(self.base.__class__.__name__,
                             self.base.id)
        self.storage.save()
        with open(self.file_path, "r", encoding="UTF-8") as file:
            data = json.load(file)
        self.assertIn(key, data)

    def test_reload(self):
        """tests the reload method
        """
        self.storage.new(self.base)
        self.storage.save()
        self.storage.reload()
        key = self.base.__class__.__name__ + "." + self.base.id
        self.assertIn(key, self.storage.all())
if __name__ == "__main__":
    unittest.main()
