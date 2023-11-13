#!/usr/bin/python3
"""Unittest for BaseModel Class."""

from models import storage
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from datetime import datetime
import json
import os
import re
import time
import unittest
import uuid


class TestBaseModel(unittest.TestCase):

    """ All Test Cases for the BaseModel"""

    def setUp(self):
        """Sets up test """
        pass

    def tearDown(self):
        """Tears down test """
        self.resetStorage()
        pass

    def resetStorage(self):
        """Resets FileStorage data."""
        FileStorage._FileStorage__objects = {}
        if os.path.isfile(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_3_instantiation(self):
        """Tests instantiation of BaseModel class."""

        base = BaseModel()
        self.assertEqual(str(type(base)), "<class 'models.base_model.BaseModel'>")
        self.assertIsInstance(b, BaseModel)
        self.assertTrue(issubclass(type(b), BaseModel))

    def test_3_init_no_args(self):
        """Tests __init__ with no arguments."""
        self.resetStorage()
        with self.assertRaises(TypeError) as error:
            BaseModel.__init__()
        note = "__init__() missing 1 required positional argument: 'self'"
        self.assertEqual(str(e.exception), note)

    def test_3_init_many_args(self):
        """Tests __init__ with many arguments."""
        self.resetStorage()
        args = [i for i in range(1000)]
        base = BaseModel(0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
        base = BaseModel(*args)

    def test_3_attributes(self):
        """Tests attributes value for instance of a BaseModel class."""

        attributes = storage.attributes()["BaseModel"]
        obj = BaseModel()
        for key, val in attributes.items():
            self.assertTrue(hasattr(obj, key))
            self.assertEqual(type(getattr(obj, key, None)), val)

    def test_3_datetime_created(self):
        """Tests if updated_at & created_at are current at creation."""
        date_now = datetime.now()
        base = BaseModel()
        diff = base.updated_at - base.created_at
        self.assertTrue(abs(diff.total_seconds()) < 0.01)
        diff = base.created_at - date_now
        self.assertTrue(abs(diff.total_seconds()) < 0.1)

    def test_3_id(self):
        """Tests for unique user ids."""

        nl = [BaseModel().id for i in range(1000)]
        self.assertEqual(len(set(nl)), len(nl))

    def test_3_save(self):
        """Tests the public instance method save()."""

        base = BaseModel()
        time.sleep(0.5)
        date_now = datetime.now()
        base.save()
        diff = base.updated_at - date_now
        self.assertTrue(abs(diff.total_seconds()) < 0.01)

    def test_3_str(self):
        """Tests for __str__ method."""
        base = BaseModel()
        rex = re.compile(r"^\[(.*)\] \((.*)\) (.*)$")
        res = rex.match(str(b))
        self.assertIsNotNone(res)
        self.assertEqual(res.group(1), "BaseModel")
        self.assertEqual(res.group(2), base.id)
        s = res.group(3)
        s = re.sub(r"(datetime\.datetime\([^)]*\))", "'\\1'", s)
        d = json.loads(s.replace("'", '"'))
        d2 = b.__dict__.copy()
        d2["created_at"] = repr(d2["created_at"])
        d2["updated_at"] = repr(d2["updated_at"])
        self.assertEqual(d, d2)

    def test_3_to_dict(self):
        """Tests the public instance method to_dict()."""

        base = BaseModel()
        base.name = "Laura"
        base.age = 23
        d = base.to_dict()
        self.assertEqual(d["id"], base.id)
        self.assertEqual(d["__class__"], type(b).__name__)
        self.assertEqual(d["created_at"], base.created_at.isoformat())
        self.assertEqual(d["updated_at"], base.updated_at.isoformat())
        self.assertEqual(d["name"], base.name)
        self.assertEqual(d["age"], base.age)

    def test_3_to_dict_no_args(self):
        """Tests to_dict() with no arguments."""
        self.resetStorage()
        with self.assertRaises(TypeError) as error:
            BaseModel.to_dict()
        note = "to_dict() missing 1 required positional argument: 'self'"
        self.assertEqual(str(error.exception), note)

    def test_3_to_dict_excess_args(self):
        """Tests to_dict() with too many arguments."""
        self.resetStorage()
        with self.assertRaises(TypeError) as error:
            BaseModel.to_dict(self, 98)
        note = "to_dict() takes 1 positional argument but 2 were given"
        self.assertEqual(str(error.exception), note)

    def test_4_instantiation(self):
        """Tests instantiation with **kwargs."""

        my_model = BaseModel()
        my_model.name = "Holberton"
        my_model.my_number = 89
        my_model_json = my_model.to_dict()
        my_new_model = BaseModel(**my_model_json)
        self.assertEqual(my_new_model.to_dict(), my_model.to_dict())

    def test_4_instantiation_dict(self):
        """Tests instantiation with **kwargs from custom dict."""
        d = {"__class__": "BaseModel",
             "updated_at":
             datetime(2050, 12, 30, 23, 59, 59, 123456).isoformat(),
             "created_at": datetime.now().isoformat(),
             "id": uuid.uuid4(),
             "var": "foobar",
             "int": 108,
             "float": 3.14}
        obj = BaseModel(**d)
        self.assertEqual(obj.to_dict(), d)

    def test_5_save(self):
        """Tests that storage.save() is called from save()."""
        self.resetStorage()
        base = BaseModel()
        base.save()
        key = "{}.{}".format(type(b).__name__, base.id)
        d = {key: base.to_dict()}
        self.assertTrue(os.path.isfile(FileStorage._FileStorage__file_path))
        with open(FileStorage._FileStorage__file_path,
                  "r", encoding="utf-8") as file:
            self.assertEqual(len(file.read()), len(json.dumps(d)))
            file.seek(0)
            self.assertEqual(json.load(f), d)

    def test_5_save_no_args(self):
        """Tests save() with no arguments."""
        self.resetStorage()
        with self.assertRaises(TypeError) as error:
            BaseModel.save()
        msg = "save() missing 1 required positional argument: 'self'"
        self.assertEqual(str(error.exception), msg)

    def test_5_save_excess_args(self):
        """Tests save() with too many arguments."""
        self.resetStorage()
        with self.assertRaises(TypeError) as error:
            BaseModel.save(self, 98)
        msg = "save() takes 1 positional argument but 2 were given"
        self.assertEqual(str(error.exception), msg)


if __name__ == '__main__':
    unittest.main()
