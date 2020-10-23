#!/usr/bin/python3
from user import User 
from challenge import Challenge
class Team:
    def __init__(self, name, users = [], role_id = None):
        self.name = name
        self.members = users
        self.role_id = role_id

    def add_user(self, user: User):
        self.members.append(user)
    
    def kick_user(self, user: User):
        self.members.remove(user)