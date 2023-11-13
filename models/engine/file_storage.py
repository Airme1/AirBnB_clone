#!/usr/bin/python3
import json
import datetime

"""
Module to store data created in python program
and to help in serialization and deserialization
"""


class FileStorage():
    """initialization of fileStorage to work"""

    __file_path = "file.json"
    __objects = {}            

    def all(self):
        """returns dictionary form of object"""
        return FileStorage.__objects
    
    def new(self, obj):
        """methods sets in the obj with key <obj class name>.id
        which will be appended to __objects dictionary
        """
        obj_key = "{}.{}".format(obj.__class__.__name__, obj.id)
    
    def save(self):
        """serializes __objects to the 
        JSON file (path: __file_path)
        """
        a_dictionary = {}
        for key, value in FileStorage.__object.items():
            a_dictionary[key] = value.to_dict()
        with open(FileStorage.__file_path, "w") as file:
            json.dump(a_dictionary, file)

    def reload(self):
         """deserializes the JSON file to __objects 
         (only if the JSON file (__file_path) exists ;
         """
         try:
            with open(FileStorage.__file_path, "r") as file:
                a_dictionary = json.load(FileStorage.__file_path)
        except Exception as error:
            pass