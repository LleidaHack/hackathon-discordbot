import unittest

from discord.ext.commands import Context

from src.crud.firebase import Firebase
from src.modules.commands.invite import InviteCommand


class MockContext(Context):

    def __init__(self, **attrs):
        pass


class MockFirebase(Firebase):

    def __init__(self, **attrs):
        pass


class TestInviteCommand(unittest.TestCase):

    def setUp(self):
        self.invite = InviteCommand(MockContext(), MockFirebase())

    def test_people_arguments(self):
        name = 'Elena Barrachina#1234'
        self.assertEqual([name.split('#')], self.invite.get_people_names(f'eps!invite {name}'))
