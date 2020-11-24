#!/usr/bin/python3
import logging
import os
from functools import wraps
from typing import List, Optional

import discord
from discord import Member
from discord.ext import commands as discord_commands
from discord.ext.commands import Context

from src.crud.firebase import Firebase
from src.models.group import Group
from src.models.user import User as ModelUser
from src.modules.commands.create import CreateCommand
from src.modules.commands.invite import InviteCommand
from src.modules.commands.leave import LeaveCommand
from src.modules.commands.login import LoginCommand
from src.modules.commands.join import JoinCommand
from src.modules.commands.question_ask import AskCommand, ReplyCommand
from src.modules.login import StartLogin, FinishLogin
from src.modules.pools.authentication import AuthenticationPool
from src.modules.pools.questions import QuestionPool
from src.modules.utils import GroupCreator

DB = Firebase()


def group_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        import src.texts.auth as txt
        ctx = args[1]
        user = DB.get_user(discord_id=ctx.message.author.id)
        if user.group_name is None:
            logging.info("Usuario sin grupo")
            await ctx.send(txt.NOT_INGROUP_ERROR(ctx.author))
            return
        logging.info(f"Usuario con grupo")
        return await func(*args)

    return wrapper


class DiscordBot:
    def __init__(self):
        logging.info("Reading bot config data")

        intents = discord.Intents.all()
        self.client = discord_commands.Bot(os.getenv('DISCORD_PREFIX'), guild_subscriptions=True, intents=intents)
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
        async def ask(ctx, question):
            await AskCommand(ctx, question, self.questions, self.client).apply()

        @self.client.command()
        async def reply(ctx, num, reply):
            await ReplyCommand(ctx, self.questions, num, reply).apply()

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

    def start(self):
        logging.info("Starting bot!")
        self.client.run(self.token)

    async def join_command(self, ctx):
        from src.modules.facades import ContextFacade
        import src.texts.join_texts as txt
        if not ctx.guild:
            ctx.guild = self.client.get_guild(int(os.getenv('GUILD')))
            ctx.author = ctx.guild.get_member(ctx.author.id)

        fac: ContextFacade = ContextFacade(ctx)
        logging.info(f"join command por {fac.get_author().name}")
        user: ModelUser = DB.get_user_from_id(fac.get_author().id)
        if user.group_name is not None:
            logging.error(f"User {fac.get_author().name} ya está en un grupo: {user.group_name}")
            await ctx.send(txt.USER_ALREADY_IN_TEAM(user.group_name))
        msg = fac.get_message().split()
        if len(msg) == 1:
            invitations = DB.get_invitations(user.discord_id)
            if len(invitations) > 1:
                logging.error(
                    f"User {fac.get_author().name} tiene más de una invitacion pero no ha especificado equipo.")
                await ctx.send(txt.MANY_INVITES(list(map(lambda x: x.group_name, invitations))))
                return
            if len(invitations) == 0:
                logging.error(f"User {fac.get_author().name} no tiene ninguna invitacion.")
                await ctx.send(txt.ANY_INVITE(user.username, user.discriminator))
                return
            group_name = invitations[0].group_name
            invitation = invitations[0]
        else:
            group_name = fac.get_message().split()[1]
            invitation = DB.get_invitation(user.discord_id, group_name)

        if not invitation:
            logging.error(f"User {fac.get_author().name} no tiene invitaciones del grupo {group_name}.")
            await ctx.send(txt.NOT_ALLOWED_TEAM(group_name))
            return
        _, invitation = invitation
        if invitation.group_name != group_name:
            logging.error(f"Illegal Statement: {group_name} must be {invitation.group_name}")
            await ctx.send(txt.ERROR_SERVER)
            return
        logging.info(f"{fac.get_author().name} invitation del grupo {group_name}")
        if not DB.accept_invitation(invitation.user_id, invitation.group_name):
            logging.error(f"Invitación no encontrada")
            await ctx.send(txt.ERROR_SERVER)
            return
        group = DB.get_group(invitation.group_name)
        group.add_user(user.discord_id)
        DB.create_or_update_group(group)
        user.group_name = group_name
        DB.create_or_update_user(user)
        guild = ctx.guild
        role = discord.utils.get(guild.roles, name=group.name)
        member = guild.get_member(user.discord_id)
        logging.info(f"Añadiendo el rol {role.name} al miembro {member.name}")
        await member.add_roles(role)
        await ctx.send(txt.MEMBER_REGISTERED_IN(member.name, role.name))

    @group_required
    async def leave_command(self, ctx):
        from src.modules.facades import ContextFacade
        import src.texts.leave_texts as txt
        if not ctx.guild:
            ctx.guild = self.client.get_guild(int(os.getenv('GUILD')))
            ctx.author = ctx.guild.get_member(ctx.author.id)
        fac: ContextFacade = ContextFacade(ctx)
        logging.info(f"leave command por {fac.get_author().name}")
        user: ModelUser = DB.get_user_from_id(fac.get_author().id)
        group = DB.get_group(user.group_name)
        if not group:
            logging.error(f"No se ha encontrado el grupo {user.group_name} del usuario {user.get_full_name()}.")
            await ctx.send(txt.SERVER_ERROR)
            return
        group.remove_user(user.discord_id)
        user.group_name = None
        DB.create_or_update_user(user)
        DB.create_or_update_group(group)
        role = discord.utils.get(ctx.guild.roles, name=group.name)
        member = ctx.guild.get_member(user.discord_id)
        await member.remove_roles(role)
        if group.size() == 0:
            chanels = list(filter(lambda x: role in x.overwrites, ctx.guild.channels))
            # if the channel exists
            for chanel in chanels:
                await chanel.delete()
            DB.delete_group(group.name)
            await role.delete()
        await ctx.send(txt.LEAVE_MSG(member.name, role.name))
