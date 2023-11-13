#!/usr/bin/python3

from models.base_model import BaseModel


class Review(BaseModel):
    """Storing review for places for a user"""
    place_id = ""
    user_id = ""
    text = ""