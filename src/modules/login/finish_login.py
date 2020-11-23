import logging

import discord
from discord import User

import src.texts.login_text as login_texts
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

    async def finish_login(self, user: User, email: str):
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

    async def register(self, email, web_group, user, web_user):
        logging.info(f"Usuario localizado {web_user.nickname}")
        discord_user = self.DB.get_user(email=email)
        if discord_user:
            await user.send(login_texts.REGISTER_ALREADY_REGISTER)
            return
        member = self.guild.get_member(user.id)
        logging.info(f"Miembro de la Guild: {member.nick}")
        discord_user = await self.get_discord_user(email, web_group, member, user)
        role_hacker = discord.utils.get(self.guild.roles, name=self.hacker_role)
        await member.add_roles(role_hacker)
        self.DB.create_or_update_user(discord_user)
        await user.send(login_texts.REGISTER_OK)

    async def get_discord_user(self, email, web_group, member, user):
        if not web_group:
            return await self.get_alone_user(email, user)
        return await self.get_user_of_group(email, web_group, member, user)

    async def get_user_of_group(self, email, web_group, member, user):
        discord_group = self.DB.get_group(web_group.name)
        if discord_group:
            logging.info(f"Se ha detectado el grupo {discord_group} en Firebase")
            role = discord.utils.get(self.guild.roles, name=web_group.name)
            logging.info(f"[REGISTER - OK] Añadiendo el usuario {member} al rol {role}")
            discord_group.members.append(user.id)
            await member.add_roles(role)
            self.DB.create_or_update_group(discord_group)
        else:
            logging.info(f"Se creará {discord_group} y con sus roles")
            await self.group_creator.create_group(web_group, member)
        discord_user = ModelUser(user.name, user.discriminator, user.id, web_group.name, email)
        await user.send(login_texts.USER_HAS_GROUP(discord_group.name))
        return discord_user

    async def get_alone_user(self, email, user):
        discord_user = ModelUser(user.name, user.discriminator, user.id, None, email)
        await user.send(login_texts.USER_NO_GROUP(user.name, user.discriminator))
        return discord_user
