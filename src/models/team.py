#!/usr/bin/python3
from user import User 
from challenge import Challenge
class Team:
    def __init__(self, name):
        self.name = name
        self.members = []
        self.challenges = []
        break

    def add_user(self, user: User):
        self.members.append(user)
    
    def kick_user(self, user: User):
        self.members.remove(user)
    
    def join_challenge(self, challenge: Challenge):
        self.challenges.append(Challenge)
    
    def leave_challenge(self, challenge: Challenge):
        self.challenges.remove(Challenge)
