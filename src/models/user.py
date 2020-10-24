#!/usr/bin/python3
from team import Team
class User:
    def __init__(self, username, discrminator, discord_id=None, group_name, email):
        self.username = username
        self.discrminator = discrminator
        self.discord_id = discord_id
        self.group_name = group_name
        self.email = email
    @staticmethod
    def from_dict(dict):
        # return User(dict['fullName'],dict['email'],dict['githubUrl'],dict['nickname'])
        pass
