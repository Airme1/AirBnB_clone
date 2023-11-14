#!/usr/bin/python3
"""Create City class for airbnb"""
from models.base_model import BaseModel


class City(BaseModel):
    """Contains information for city"""
    state_id = ""
    name = ""
