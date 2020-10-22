#!/usr/bin/python3
from team import Team
class User:
    def __init__(self, username, discrminator, discord_id, team, group_name):
        self.username = username
        self.discrminator = discrminator
        self.discord_id = discord_id
        self.team = team
        self.group_name = group_name
        
    def join_group(self, team: Team):
        if (self.team):
            self.team.kick_user(self)
        self.team = team
    