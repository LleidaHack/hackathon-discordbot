import logging, discord
from discord import Guild, User, Role

from src.models.group import Group

class CreateGroup:
    def __init__(self, category_id: str, database: Firebase, group: Group, user: User, guild: Guild):
        self.category = category_id
        self.database = database
        self.group = group
        self.guild = guild
        self.user = user
    async def create_group(self):


        logging.info("[CREATE GROUP - OK] Creando rol")
        role = await self.guild.create_role(name=self.group.name)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            role: discord.PermissionOverwrite(read_messages=True)
        }
        logging.info("[CREATE GROUP - OK] Localizando categoria de equipos")
        for cat in guild.categories:
            if str(cat.id) == self.category:
                logging.info("[CREATE GROUP - OK] Creando canales de chat y voz")
                await guild.create_text_channel(group.name, overwrites=overwrites, category=cat)
                await guild.create_voice_channel(group.name, overwrites=overwrites, category=cat)
                break


        logging.info("[CREATE GROUP - OK] Añadiendo usuario")
        await self.add_user()
        logging.info("[CREATE GROUP - OK] Creando grupo en la base de datos")
        self.database.create_or_update_group(group)

        return True

    async def add_user(self, role: Role):
        await self.user.add_roles(role)
        user = self.database.get_user(discord_id= self.user.id)
        user.group_name = self.group.name
        self.group.members.append(user)

        self.database.create_or_update_user(user)
        pass