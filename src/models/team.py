#!/usr/bin/python3
class Team:
    def __init__(self, name, users = [], role_id = None):
        self.group_name = name
        self.members = users
        self.role_id = role_id