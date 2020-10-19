#!/usr/bin/python3
from team import Team
class User:
    def __init__(self, full_name, email, github, nickname, team: Team ):
        self.full_name = full_name
        self.email = email
        self.github = github
        self.nickname = nickname
        self.team = team
        break
    def join_group(self, team: Team):
        if (self.team):
            self.team.kick_user(self)
        self.team = team
    