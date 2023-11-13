#!/usr/bin/python3
"""Unittest module for the Review Class."""

import unittest
from datetime import datetime
import time
from models.review import Review
import re
import json
from models.engine.file_storage import FileStorage
import os
from models import storage
from models.base_model import BaseModel


class TestReview(unittest.TestCase):

    """Test Cases for the Review class."""

    def setUp(self):
        """Sets up test methods."""
        pass

    def tearDown(self):
        """Tears down test methods."""
        self.resetStorage()
        pass

    def resetStorage(self):
        """Resets FileStorage data."""
        FileStorage._FileStorage__objects = {}
        if os.path.isfile(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_8_instantiation(self):
        """Tests instantiation of Review class."""

        base = Review()
        self.assertEqual(str(type(base)), "<class 'models.review.Review'>")
        self.assertIsInstance(base, Review)
        self.assertTrue(issubclass(type(base), BaseModel))

    def test_8_attributes(self):
        """Tests the attributes of Review class."""
        attributes = storage.attributes()["Review"]
        obj = Review()
        for key, val in attributes.items():
            self.assertTrue(hasattr(obj, key))
            self.assertEqual(type(getattr(obj, key, None)), val)


if __name__ == "__main__":
    unittest.main()
