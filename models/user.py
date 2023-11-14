#!/usr/bin/python3

from base_model import BaseModel


class User(BaseModel):
    """information of User stored"""
    email = ""
    password = ""
    first_name = ""
    last_name = ""
