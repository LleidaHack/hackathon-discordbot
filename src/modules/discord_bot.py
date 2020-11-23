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
from src.modules.commands.question_ask import AskCommand, ReplyCommand
from src.modules.pools.questions import QuestionPool

DB = Firebase()


def authorization_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        import src.texts.auth as txt
        ctx = args[1]
        user = DB.get_user(discord_id=ctx.message.author.id)
        if user is None:
            logging.info("Usuario no registrado")
            await ctx.send(txt.NOT_REGISTERED_ERROR)
            return
        logging.info(f"Usuario registrado")
        return await func(*args)

    return wrapper


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
        self.user_registering = {}

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
            await self.start_register(ctx.author, ctx)

        @self.client.command()
        async def create(ctx):
            await self.create_command(ctx)

        @self.client.command()
        async def invite(ctx):
            await self.invite_command(ctx)

        @self.client.command()
        async def join(ctx):
            await self.join_command(ctx)

        @self.client.command()
        async def leave(ctx):
            await self.leave_command(ctx)

        @self.client.event
        async def on_member_join(member):
            import src.texts.login_text as login_texts
            await member.send(embed=login_texts.WELCOME_MESSAGE)
            await self.start_register(member)

        @self.client.listen('on_message')
        async def on_message(message):
            if message.author in self.user_registering and not message.guild and not message.author.bot:
                logging.info(f"Email enviado: {message.content}")
                await self.login(message.author, message.content, message.guild)
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

    async def start_register(self, author, ctx=None):
        import src.texts.login_text as login_texts
        if ctx and ctx.guild:
            await ctx.send(login_texts.PM_SENDED)
        user_discord = DB.get_user(discord_id=author.id)
        if not user_discord:
            logging.info("Enviando mensaje de inicio de registro a " + str(author))
            await author.send(login_texts.REGISTER_MESSAGE)
            self.user_registering[author] = 0
        else:
            await author.send(login_texts.REGISTER_ALREADY_REGISTER)

    async def login(self, user, email, guild):
        import src.texts.login_text as login_texts
        logging.info("Email test")
        await user.send(login_texts.REGISTER_STARTING)
        web_user, group = DB.recover_web_group_by_user(email)
        if web_user:
            logging.info(f"Usuario localizado {web_user.nickname}")
            discord_user = DB.get_user(email=email)
            if discord_user:
                await user.send(login_texts.REGISTER_ALREADY_REGISTER)
                pass
            else:
                guild = self.client.get_guild(int(os.getenv('GUILD')))
                member = guild.get_member(user.id)
                logging.info(f"Miembro de la Guild: {member.nick}")
                if not guild:
                    return
                if group:
                    discord_group = DB.get_group(group.name)
                    logging.info(f"Se ha detectado el grupo {discord_group}")
                    if not discord_group:
                        await  self.create_group_on_server(group, member, guild)
                        discord_group = DB.get_group(group.name)
                    role = discord.utils.get(guild.roles, name=group.name)

                    discord_group.members.append(user.id)
                    DB.create_or_update_group(discord_group)
                    discord_user = ModelUser(user.name, user.discriminator, user.id, group.name, email)
                    logging.info(f"[REGISTER - OK] Añadiendo el usuario {member} al rol {role}")
                    await member.add_roles(role)
                    await user.send(login_texts.USER_HAS_GROUP(discord_group.name))

                else:
                    discord_user = ModelUser(user.name, user.discriminator, user.id, None, email)
                    await user.send(login_texts.USER_NO_GROUP(user.name, user.discriminator))

                role_hacker = discord.utils.get(guild.roles, name=os.getenv("HACKER_ROLE"))
                await member.add_roles(role_hacker)

                DB.create_or_update_user(discord_user)
                # Creacion usuario
                await user.send(login_texts.REGISTER_OK)
        else:
            logging.info("No se ha encontrado al usuario")
            await user.send(login_texts.REGISTER_KO)
        self.user_registering.pop(user)

    @authorization_required
    async def create_command(self, ctx):
        import src.texts.create_texts as texts
        if not ctx.guild:
            ctx.guild = self.client.get_guild(int(os.getenv('GUILD')))
            ctx.author = ctx.guild.get_member(ctx.author.id)

        user = DB.get_user(discord_id=ctx.message.author.id)
        if user.group_name is not None and user.group_name != '':
            logging.info("[COMMAND CREATE - ERROR] El usuario ya se encuentra en un grupo")
            await ctx.send(texts.ALREADY_ON_GROUP_ERROR)
            return
        command = ctx.message.content.split()
        if len(command) < 2:
            logging.info("[COMMAND CREATE - ERROR] La sintaxis es incorrecta")
            await ctx.send(texts.SINTAXIX_ERROR)
            return
        group = DB.get_group(group_name=' '.join(command[1:]))
        if not group:
            group = DB.recover_web_group(' '.join(command[1:]))
        if group:
            logging.info("[COMMAND CREATE - ERROR] El grupo indicado ya existe")
            await ctx.send(texts.GROUP_ALREADY_EXISTS_ERROR)
            return
        await ctx.send(texts.STARTING_CREATE_GROUP)
        group = Group(' '.join(command[1:]), [ctx.message.author.id])
        await self.create_group_on_server(group, ctx.author, ctx.guild)
        user.group_name = group.name
        DB.create_or_update_user(user)
        logging.info("[COMMAND CREATE - OK] Informando all Ok")
        await ctx.send(texts.CREATED_GROUP)

    @authorization_required
    @group_required
    async def invite_command(self, ctx: Context):
        import src.texts.invite_texts as txt
        if not ctx.guild:
            ctx.guild = self.client.get_guild(int(os.getenv('GUILD')))
        username: str = ctx.author.name
        logging.info(f"Comando 'invite' recibido por usuario {username}")
        group: Optional[Group] = DB.get_group(DB.get_user(ctx.author.id).group_name)
        people = list(map(lambda x: x.split('#'), ctx.message.content.split()[1:]))
        people: List[ModelUser] = list(map(lambda x: DB.get_user(username=x[0], discriminator=x[1]), people))
        if not any(people):
            logging.error("Gente no encontrada.")
            await ctx.send(txt.NOT_FOUND_PEOPLE)
            return

        people = list(filter(lambda x: x is not None or not "", people))
        logging.info(f"Gente encontrada: {[p.username for p in people]}")
        if group.size() + len(people) > 4:
            logging.error(
                f"Usuario {username} quiere añadir al grupo {group.name} {len(people)} personas pero ya son {group.size()}")
            await ctx.send(txt.TEAM_OVERFLOW)
            return
        for already_member in filter(lambda x: x.group_name is not None, people):
            logging.info(f"{already_member} está ya en otro grupo: {already_member.group_name}")
            await ctx.send(txt.ALREADY_IN_A_GROUP(already_member.username, already_member.group_name))
        people = list(filter(lambda x: x.group_name is None, people))
        guild = ctx.guild
        role = discord.utils.get(guild.roles, name=group.name)
        if not role:
            logging.error(f"Not found role {group.name}")
            return
        for p in people:
            member: Member = guild.get_member(p.discord_id)
            DB.create_invitation(p.discord_id, group.name)
            await member.send(
                f"Has sido invitado al grupo {group.name}\nPara formar parte del grupo usa el comando eps!join {group.name}")

    @authorization_required
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

    @authorization_required
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

    async def create_group_on_server(self, group, user, guild):
        logging.info("[COMMAND CREATE - OK] Solicitando creacion de grupo")
        DB.create_or_update_group(group)
        logging.info("[COMMAND CREATE - OK] Creando rol")

        await guild.create_role(name=group.name)
        role = discord.utils.get(guild.roles, name=group.name)
        logging.info("[COMMAND CREATE - OK] Añadiendo el usuario al rol")
        await user.add_roles(role)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            role: discord.PermissionOverwrite(read_messages=True)
        }
        logging.info("[COMMAND CREATE - OK] Localizando categoria de equipos")

        for cat in guild.categories:
            if str(cat.id) == os.getenv('TEAMS_CATEGORY_ID'):
                logging.info("[COMMAND CREATE - OK] Creando canales de chat y voz")
                await guild.create_text_channel(group.name, overwrites=overwrites, category=cat)
                await guild.create_voice_channel(group.name, overwrites=overwrites, category=cat)
                break
