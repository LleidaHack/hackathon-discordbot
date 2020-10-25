#!/usr/bin/python3
from team import Team


class WebUser:
    def __init__(self, accepted, birthDate, displayName, email, fullName, githubUrl, nickname):
        self.accepted = accepted
        self.birthDate = birthDate
        self.displayName = displayName
        self.email = email
        self.fullName = fullName
        self.githubUrl = githubUrl
        self.nickname = nickname
