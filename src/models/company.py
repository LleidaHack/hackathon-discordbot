#!/usr/bin/python3
from user import User
class Company:
    def __init__(self, name):
        self.name = name
        self.users = []
        break

    def add_user(self, user: User):
        self.users.append(user)

    def remove_user(self, user:User):
        self.users.remove(user)
