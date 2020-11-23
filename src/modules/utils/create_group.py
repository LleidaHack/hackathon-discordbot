import logging

import discord
from discord import Guild, Role, Member

from src.crud.firebase import Firebase
from src.models.group import Group
from src.models.user import User


class GroupCreator:
    def __init__(self, category_id: str, database: Firebase, guild: Guild):
        self.category = category_id
        self.database = database
        self.guild: Guild = guild

    async def create_group(self, group: Group, member: Member, modal_user: User):
        logging.info("[CREATE GROUP - OK] Creando rol")
        role = await self.guild.create_role(name=group.name)
        await self.create_channel_permissions(role, group)
        logging.info(f"[CREATE GROUP - OK] Añadiendo {member} al rol {role}")
        await member.add_roles(role)
        logging.info("[CREATE GROUP - OK] Añadiendo usuario")
        await self.add_user_and_update(group, modal_user)

    async def create_channel_permissions(self, role: Role, group: Group):
        overwrites = {
            self.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            role: discord.PermissionOverwrite(read_messages=True)
        }
        for cat in self.guild.categories:
            if str(cat.id) == self.category:
                logging.info("[CREATE GROUP - OK] Creando canales de chat y voz")
                await self.guild.create_text_channel(group.name, overwrites=overwrites, category=cat)
                await self.guild.create_voice_channel(group.name, overwrites=overwrites, category=cat)
                break

    async def add_user_and_update(self, group: Group, modal_user: User):
        await self.update_user_database(group, modal_user)

    async def update_user_database(self, group: Group, user: User):
        user.group_name = group.name
        group.add_user(user.discord_id)
        logging.info(f"[CREATE GROUP - OK] User {user} en la base de datos")
        self.database.create_or_update_user(user)
        logging.info(f"[CREATE GROUP - OK] Creando grupo {group} en la base de datos")
        self.database.create_or_update_group(group)

