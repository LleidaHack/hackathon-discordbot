import logging

import discord
from discord import User

import src.texts.login_text as login_texts
from src.modules.pools.authentication import AuthenticationPool
from src.models.user import User as ModelUser


class StartLogin:

    def __init__(self, db, pool):
        self.DB = db
        self.pool = pool

    async def start_login(self, author: User):
        user_discord = self.DB.get_user(discord_id=author.id)
        if not user_discord:
            logging.info("Enviando mensaje de inicio de registro a " + str(author))
            await author.send(login_texts.REGISTER_MESSAGE)
            self.pool.add_newbie(author)
        else:
            await author.send(login_texts.REGISTER_ALREADY_REGISTER)


class FinishLogin:

    def __init__(self, guild, db, pool: AuthenticationPool, hacker_role: str):
        self.guild = guild
        self.DB = db
        self.pool = pool
        self.hacker_role = hacker_role

    async def finish_login(self, user: User, email: str):
        import src.texts.login_text as login_texts
        logging.info("Email test")
        await user.send(login_texts.REGISTER_STARTING)
        web_user, group = self.DB.recover_web_group_by_user(email)
        if web_user:
            await self.register(email, group, user, web_user)
        else:
            logging.info("No se ha encontrado al usuario")
            await user.send(login_texts.REGISTER_KO)
        self.pool.finish_login(user)

    async def register(self, email, group, user, web_user):
        logging.info(f"Usuario localizado {web_user.nickname}")
        discord_user = self.DB.get_user(email=email)
        if discord_user:
            await user.send(login_texts.REGISTER_ALREADY_REGISTER)
            return
        member = self.guild.get_member(user.id)
        logging.info(f"Miembro de la Guild: {member.nick}")
        if group:
            discord_group = self.DB.get_group(group.name)
            logging.info(f"Se ha detectado el grupo {discord_group}")
            if not discord_group:
                await self.create_group_on_server(group, member, self.guild)
                discord_group = self.DB.get_group(group.name)
            role = discord.utils.get(self.guild.roles, name=group.name)
            discord_group.members.append(user.id)
            self.DB.create_or_update_group(discord_group)
            discord_user = ModelUser(user.name, user.discriminator, user.id, group.name, email)
            logging.info(f"[REGISTER - OK] Añadiendo el usuario {member} al rol {role}")
            await member.add_roles(role)
            await user.send(login_texts.USER_HAS_GROUP(discord_group.name))

        else:
            discord_user = ModelUser(user.name, user.discriminator, user.id, None, email)
            await user.send(login_texts.USER_NO_GROUP(user.name, user.discriminator))

        role_hacker = discord.utils.get(self.guild.roles, name=self.hacker_role)
        await member.add_roles(role_hacker)

        self.DB.create_or_update_user(discord_user)
        # Creacion usuario
        await user.send(login_texts.REGISTER_OK)
