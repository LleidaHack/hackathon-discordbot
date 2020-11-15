#!/usr/bin/python3
from typing import List

from src.models.team import Team


class User:
    def __init__(self, username, discrminator, discord_id, group_name, email):
        self.username = username
        self.discriminator = discrminator
        self.discord_id = discord_id
        self.group_name = group_name
        self.email = email
