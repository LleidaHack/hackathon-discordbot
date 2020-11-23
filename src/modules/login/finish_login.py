import logging
from typing import Optional

import discord
from discord import User as DiscordUser

import src.texts.login_text as login_texts
from src.models.group import Group
from src.models.user import User as ModelUser
from src.modules.pools.authentication import AuthenticationPool
from src.modules.utils import GroupCreator


class FinishLogin:

    def __init__(self, guild, db, pool: AuthenticationPool, hacker_role: str, group_creator: GroupCreator):
        self.guild = guild
        self.DB = db
        self.pool = pool
        self.hacker_role = hacker_role
        self.group_creator = group_creator

    async def finish_login(self, user: DiscordUser, email: str):
        import src.texts.login_text as login_texts
        logging.info("Email test")
        await user.send(login_texts.REGISTER_STARTING)
        web_user, web_group = self.DB.recover_web_group_by_user(email)
        if web_user:
            await self.register(email, web_group, user, web_user)
        else:
            logging.info("No se ha encontrado al usuario")
            await user.send(login_texts.REGISTER_KO)
        self.pool.finish_login(user)

    async def register(self, email, web_group, discord_user: DiscordUser, web_user):
        logging.info(f"Usuario localizado {web_user.nickname}")
        firebase_user = self.DB.get_user(email=email)
        if firebase_user:
            await discord_user.send(login_texts.REGISTER_ALREADY_REGISTER)
            return
        member = self.guild.get_member(discord_user.id)
        logging.info(f"Miembro de la Guild: {member.nick}")
        await self.create_discord_user(email, web_group, member, discord_user)
        await self.add_hacker_role(member)
        await discord_user.send(login_texts.REGISTER_OK)

    async def add_hacker_role(self, member):
        role_hacker = discord.utils.get(self.guild.roles, name=self.hacker_role)
        await member.add_roles(role_hacker)

    async def create_discord_user(self, email, web_group, member, discord_user):
        if not web_group:
            await self.create_alone_user(email, discord_user)
        await self.create_user_of_group(email, web_group, member, discord_user)

    async def create_user_of_group(self, email, web_group, member, discord_user: DiscordUser):
        discord_group: Optional[Group] = self.DB.get_group(web_group.name)
        if discord_group:
            logging.info(f"Se ha detectado el grupo {discord_group} en Firebase")
            await self.add_group_role(member, web_group)
            discord_group.add_user(discord_user.id)
            self.DB.create_or_update_group(discord_group)
            discord_user = ModelUser(discord_user.name, discord_user.discriminator, discord_user.id, web_group.name, email)
            self.DB.create_or_update_user(discord_user)
        else:
            logging.info(f"Se creará {web_group.name} y con sus roles")
            modal_user = ModelUser(discord_user.name, discord_user.discriminator, discord_user.id, web_group.name, email)
            await self.group_creator.create_group(web_group, member, modal_user)
            discord_group: Optional[Group] = self.DB.get_group(web_group.name)
        await discord_user.send(login_texts.USER_HAS_GROUP(discord_group.name))

    async def add_group_role(self, member, web_group):
        role = discord.utils.get(self.guild.roles, name=web_group.name)
        logging.info(f"[REGISTER - OK] Añadiendo el usuario {member} al rol {role}")
        await member.add_roles(role)

    async def create_alone_user(self, email, user):
        discord_user = ModelUser(user.name, user.discriminator, user.id, None, email)
        await user.send(login_texts.USER_NO_GROUP(user.name, user.discriminator))
        self.DB.create_or_update_user(discord_user)
