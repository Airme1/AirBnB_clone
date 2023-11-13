#!/usr/bin/python3

from models.base_model import BaseModel


class City(BaseModel):
    """Contains information for city"""
    state_id = ""
    name = ""