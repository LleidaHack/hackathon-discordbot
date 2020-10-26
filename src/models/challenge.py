#!/usr/bin/python3
from company import Company
from team import Team


class Challenge:
    def __init__(self, company: Company, icon):
        self.company = company
        self.icon = icon
        self.participants = []

    def add_participant(self, team: Team):
        self.participants.append(team)

    def remove_participant(self, team: Team):
        self.participants.remove(team)
