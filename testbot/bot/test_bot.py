import logging
import discord
import os
import distest
from distest import TestCollector
from distest import run_interactive_bot, run_dtest_bot
from discord.ext import commands as discord_commands
from discord.ext.commands import CommandInvokeError
from testbot.commands.test_ask import TestAsk
from testbot.commands.test_create import TestCreate
from testbot.commands.test_help import TestHelp
from testbot.commands.test_invite import TestInvite
from testbot.commands.test_join import TestJoin
from testbot.commands.test_joke import TestJoke
from testbot.commands.test_leave import TestLeave
from testbot.commands.test_list_questions import TestListQuestion
from testbot.commands.test_login import TestLogin
from testbot.commands.test_reply import TestReply
from testbot.commands.test_rpsls import TestRPSLS
from testbot.commands.test_utils import TestUtils


test_collector = TestCollector()

class TestBot():


    def __init__(self):
        logging.info("Reading test_bot config data")
        intents = discord.Intents.all()
        self.client = discord_commands.Bot(os.getenv('DISCORD_TEST_PREFIX'), guild_subscriptions=True, intents=intents)
        self.token = os.getenv('DISCORD_TEST_TOKEN')
    
    def start(self):
        logging.info("Starting test_bot!")
        distest.run_dtest_bot([None, os.getenv('LOBOT_ID'), os.getenv('DISCORD_TEST_TOKEN')],test_collector)

    #Test Comands

    @test_collector()
    async def test_ask(self, interface):
        await TestAsk(interface).run_tests()

    @test_collector()
    async def test_reply(self, interface):
        await TestReply(interface).run_tests()

    @test_collector()
    async def test_create(self, interface):
        await TestCreate(interface).run_tests()

    @test_collector()
    async def test_help(self, interface):
        await TestHelp(interface).run_tests()

    @test_collector()
    async def test_invite(self, interface):
        await TestInvite(interface).run_tests()

    @test_collector()
    async def test_join(self, interface):
        await TestJoin(interface).run_tests()

    @test_collector()
    async def test_joke(self, interface):
        await TestJoke(interface).run_tests()

    @test_collector()
    async def test_leave(self, interface):
        await TestLeave(interface).run_tests()

    @test_collector()
    async def test_list_questions(self, interface):
        await TestListQuestions(interface).run_tests()

    @test_collector()
    async def test_login(self, interface):
        await TestLogin(interface).run_tests()

    @test_collector()
    async def test_rpsls(self, interface):
        await TestRPSLS(interface).run_tests()

    @test_collector()
    async def test_utils(self, interface):
        await TestUtils(interface).run_tests()