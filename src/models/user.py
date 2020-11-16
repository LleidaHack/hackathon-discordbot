#!/usr/bin/python3

class User:
    def __init__(self, username, discriminator, discord_id, group_name, email):
        self.username = username
        self.discriminator = discriminator
        self.discord_id = discord_id
        self.group_name = group_name
        self.email = email
