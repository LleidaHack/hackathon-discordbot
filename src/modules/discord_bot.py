#!/usr/bin/python3
import logging, os
from discord.ext import commands as discord_commands, tasks
import texts.help_texts as help_texts
class DiscordBot:
    def __init__(self):
        logging.info("Reading bot config data")
        self.client = discord_commands.Bot(os.getenv('DISCORD_PREFIX'))
        self.token = os.getenv('DISCORD_TOKEN')
        self.index = 0
        self.client.remove_command('help')

        logging.info("Reading bot functions")
        @self.client.command()
        async def help(ctx):
            await self.help_command(ctx)
        pass

    def start(self):
        logging.info("Starting bot!")
        self.client.run(self.token)


    async def help_command(self, ctx):
        logging.info("Enviando mensaje de ayuda")

        await ctx.send(help_texts.GLOBAL_HELP_MESSAGE, delete_after=20)
        await ctx.author.send(embed=help_texts.EMBED_HELP_MESSAGE)