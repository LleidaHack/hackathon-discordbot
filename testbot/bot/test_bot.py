import logging
import discord
import os
from discord.ext import commands as discord_commands
from discord.ext.commands import CommandInvokeError

class TestBot():

    def __init__(self):
        logging.info("Reading test_bot config data")
        intents = discord.Intents.all()
        self.client = discord_commands.Bot(os.getenv('DISCORD_TEST_PREFIX'), guild_subscriptions=True, intents=intents)
        self.token = os.getenv('DISCORD_TEST_TOKEN')
    
    def start(self):
        logging.info("Starting test_bot!")
        self.client.run(self.token)