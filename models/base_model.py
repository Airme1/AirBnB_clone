#!/usr/bin/python3
from datetime import datetime
import uuid

"""
Base Model Class-
The Grandpa of all the Classes from which other classes
inherit their properties from
"""


class BaseModel():
    def __init__(self, *args, **kwargs):
        """Initializer for the class"""
        format_string = '%Y-%m-%dT%H:%M:%S.%f'
        if len(kwargs) > 0:
            for key, value in kwargs.items():
                if key != "__class__":
                    if key == "created_at" or key == "updated_at":
                        self.__dict__[key] = datetime.strptime(
                            value, format_string)
                    else:
                        self.__dict__[key] = value
        else:
            self.id = uuid.uuid4()
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    def __str__(self):
        """To return properties of class_name, id and dictionary"""
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__)

    def save(self):
        """to save object"""
        self.updated_at = datetime.now()
        self.created_at = datetime.now()

    def to_dict(self):
        """returns a dictionary of key/value pairs"""
        dictionary = self.__dict__.copy()
        dictionary["__class__"] = __class__.__name__
        dictionary["created_at"] = self.created_at.isoformat()
        dictionary["updated_at"] = self.updated_at.isoformat()
        return dictionary