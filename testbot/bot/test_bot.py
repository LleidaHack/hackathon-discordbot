import logging
import discord
import os
import distest
from distest import TestCollector
from distest import run_interactive_bot, run_dtest_bot
from discord.ext import commands as discord_commands
from discord.ext.commands import CommandInvokeError

class TestBot():

    test_collector = TestCollector()

    def __init__(self):
        logging.info("Reading test_bot config data")
        intents = discord.Intents.all()
        self.client = discord_commands.Bot(os.getenv('DISCORD_TEST_PREFIX'), guild_subscriptions=True, intents=intents)
        self.token = os.getenv('DISCORD_TEST_TOKEN')
    
    def start(self):
        logging.info("Starting test_bot!")
        distest.run_dtest_bot([None, os.getenv("DISCORD_TOKEN"), os.getenv('DISCORD_TEST_TOKEN')],self.token)

    #Test Comands

    @test_collector()
    def test_ask(self):
        pass

    @test_collector()
    def test_reply(self):
        pass

    @test_collector()
    def test_create(self):
        pass

    @test_collector()
    def test_help(self):
        pass

    @test_collector()
    def test_invite(self):
        pass

    @test_collector()
    def test_join(self):
        pass

    @test_collector()
    def test_joke(self):
        pass

    @test_collector()
    def test_leave(self):
        pass

    @test_collector()
    def test_list_questions(self):
        pass

    @test_collector()
    def test_login(self):
        pass

    @test_collector()
    def test_rpsls(self):
        pass

    @test_collector()
    def utils(self):
        pass