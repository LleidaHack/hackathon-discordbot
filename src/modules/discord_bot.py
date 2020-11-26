#!/usr/bin/python3
import logging
import os

import discord
from discord.ext import commands as discord_commands
from discord.ext.commands import CommandInvokeError

from src.crud.firebase import Firebase
from src.modules.commands.create import CreateCommand
from src.modules.commands.invite import InviteCommand
from src.modules.commands.join import JoinCommand
from src.modules.commands.leave import LeaveCommand
from src.modules.commands.login import LoginCommand
from src.modules.commands.list_questions import ListQuestions
from src.modules.commands.ask_reply import AskCommand, ReplyCommand
from src.modules.login import StartLogin, FinishLogin
from src.modules.pools.authentication import AuthenticationPool
from src.modules.pools.questions import QuestionPool
from src.modules.utils import GroupCreator

DB = Firebase()


class DiscordBot:
    def __init__(self):
        logging.info("Reading bot config data")

        intents = discord.Intents.all()
        self.client = discord_commands.Bot(os.getenv('DISCORD_PREFIX'), guild_subscriptions=True, intents=intents, self_bot=False)
        self.token = os.getenv('DISCORD_TOKEN')
        self.index = 0
        self.client.remove_command('help')
        logging.info("Reading bot functions")

        self.questions = QuestionPool()
        self.users_pool = AuthenticationPool()

        @self.client.command()
        async def help(ctx):
            from .commands.help import HelpCommand
            await HelpCommand(ctx).apply()

        @self.client.command()
        async def ask(ctx):
            await AskCommand(ctx, self.questions, self.client).apply()

        @self.client.command()
        async def reply(ctx, num):
            await ReplyCommand(ctx, self.questions, num).apply()

        @self.client.command()
        async def joke(ctx):
            from src.modules.commands.joke import JokeCommand
            await JokeCommand(ctx).apply()

        @self.client.command()
        async def rpsls(ctx):
            from src.modules.commands.rpsls import GameCommand
            await GameCommand(ctx).apply()

        @self.client.command()
        async def login(ctx):
            await LoginCommand(ctx, DB, ctx.author, self.users_pool).apply()

        @self.client.command()
        async def create(ctx):
            if not ctx.guild:
                ctx.guild = self.client.get_guild(int(os.getenv('GUILD')))
            group_creator: GroupCreator = GroupCreator(os.getenv('TEAMS_CATEGORY_ID'), DB, ctx.guild)
            create: CreateCommand = CreateCommand(ctx, DB, ctx.author, group_creator)
            await create.apply()

        @self.client.command()
        async def invite(ctx):
            if not ctx.guild:
                ctx.guild = self.client.get_guild(int(os.getenv('GUILD')))
            invite: InviteCommand = InviteCommand(ctx, DB)
            await invite.apply()

        @self.client.command()
        async def join(ctx):
            if not ctx.guild:
                ctx.guild = self.client.get_guild(int(os.getenv('GUILD')))
            join: JoinCommand = JoinCommand(ctx, DB)
            await join.apply()

        @self.client.command()
        async def leave(ctx):
            if not ctx.guild:
                ctx.guild = self.client.get_guild(int(os.getenv('GUILD')))
                ctx.author = ctx.guild.get_member(ctx.author.id)
            leave: LeaveCommand = LeaveCommand(ctx, DB)
            await leave.apply()

        @self.client.event
        async def on_member_join(member):
            import src.texts.login_text as login_texts
            await member.send(embed=login_texts.WELCOME_MESSAGE)
            await StartLogin(DB, self.users_pool).start_login(member)

        @self.client.event
        async def on_command_error(ctx, error):
            if isinstance(error, discord_commands.CommandError):
                from src.modules.commands.utils import CatchedError
                if isinstance(error, CommandInvokeError) and isinstance(error.original, CatchedError):
                    await ctx.send("¡Vaya! Hemos tenido un problemilla con el servidor, ya está informado :grin:")
                else:
                    await ctx.send(
                        "¿Has escrito bien el comando? Escribe `eps!help` si quieres saber los comandos :satisfied:")
            else:
                raise error

        @self.client.listen('on_message')
        async def on_message(message):
            msg: str = message.content
            if not msg.startswith("eps!") and self.users_pool.has(message.author) and \
                    not message.guild and not message.author.bot:
                logging.info(f"Email enviado: {message.content}")
                guild = self.client.get_guild(int(os.getenv('GUILD')))
                group_creator: GroupCreator = GroupCreator(os.getenv('TEAMS_CATEGORY_ID'), DB, guild)
                login_manager: FinishLogin = FinishLogin(guild, DB, self.users_pool, os.getenv("HACKER_ROLE"),
                                                         group_creator)
                await login_manager.finish_login(message.author, message.content)
                logging.info(f"Email checked: {message.content}")

        ################# ADMIN COMMANDS ###################################

        @self.client.command()
        @discord_commands.has_permissions(administrator=True)
        async def deletemsgs(ctx):
            import time
            messages = await ctx.channel.history(limit=None).flatten()
            for message in messages:
                try:
                    await message.delete()
                    time.sleep(1)
                except:
                    pass

        @self.client.command()
        @discord_commands.has_permissions(administrator=True)
        async def list_questions(ctx):
             await ListQuestions(ctx, self.questions).apply()

    def start(self):
        logging.info("Starting bot!")
        self.client.run(self.token)
