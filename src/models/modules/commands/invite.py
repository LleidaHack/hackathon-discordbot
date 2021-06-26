import logging
from typing import Optional, List

import discord
from discord import User as DiscordUser, Member
from discord.ext.commands import Context

import src.texts.invite_texts as txt
from src.crud.firebase import Firebase
from src.models.group import Group
from src.models.user import User as ModelUser
from src.modules.commands import FireBaseCommand
from src.modules.commands.command import CommandError
from src.modules.commands.utils import TraceCommand


class InviteCommand(FireBaseCommand):

    def __init__(self, context: Context, database: Firebase):
        super().__init__(context, database)

    @TraceCommand.traceback_print
    @FireBaseCommand.authorization_required
    @FireBaseCommand.group_required
    async def apply(self):
        try:
            discord_user: DiscordUser = self.ctx.author
            logging.info(f"Comando 'invite' recibido por usuario {discord_user.name}")
            group: Optional[Group] = self.DB.get_group(self.DB.get_user(discord_user.id).group_name)
            people = await self.get_people(discord_user, group)
            await self.check_role(group, self.ctx.guild)
            await self.send_msg_to_people(group, self.ctx.guild, people)
        except CommandError as er:
            logging.warning(f"Ha saltado el error {er}")
            raise er

    async def get_people(self, discord_user, group):
        people_names = self.get_people_names(self.ctx.message.content)
        people: List[ModelUser] = await self.get_DB_people(people_names)
        await self.check_group_overflow(discord_user, group, people)
        people = await self.check_people_availability(people)
        return people

    def get_people_names(self, content: str):
        start = len('eps!invite')
        content = content[start + 1:].split()
        res = []
        actual = []
        for string in content:
            actual.append(string)
            if '#' in string:
                res.append(' '.join(actual).split('#'))
                actual = []
        return res

    async def check_people_availability(self, people):
        for already_member in filter(lambda x: x.group_name is not None, people):
            logging.info(f"{already_member} está ya en otro grupo: {already_member.group_name}")
            await self.ctx.send(txt.ALREADY_IN_A_GROUP(already_member.username, already_member.group_name))
        people = list(filter(lambda x: x.group_name is None, people))
        if len(people) == 0:
            raise CommandError(msg="gente no disponible")
        return people

    async def check_group_overflow(self, discord_user, group, people):
        if group.size() + len(people) > 4:
            logging.error(
                f"Usuario {discord_user.name} quiere añadir al grupo {group.name} {len(people)} personas pero ya son {group.size()}")
            await self.ctx.send(txt.TEAM_OVERFLOW)
            raise CommandError(msg="group overflow")

    async def get_DB_people(self, people):
        people: List[ModelUser] = list(map(lambda x: self.DB.get_user(username=x[0], discriminator=x[1]), people))
        if not any(people):
            logging.error("Gente no encontrada.")
            await self.ctx.send(txt.NOT_FOUND_PEOPLE)
            raise CommandError(msg="gente no encontrada")
        people = list(filter(lambda x: x is not None or not "", people))
        logging.info(f"Gente encontrada: {[p.username for p in people]}")
        return people

    async def check_role(self, group, guild):
        role = discord.utils.get(guild.roles, name=group.name)
        if not role:
            logging.error(f"Not found role {group.name}")
            raise KeyError

    async def send_msg_to_people(self, group, guild, people):
        for p in people:
            guild_member: Member = guild.get_member(p.discord_id)
            logging.info(f"{self.ctx.author} ha invitado a {guild_member.display_name}.")
            self.DB.create_invitation(p.discord_id, group.name)
            await guild_member.send(
                f"Has sido invitado al grupo {group.name}\nPara formar parte del grupo usa el comando eps!join {group.name}")

            await self.ctx.author.send(f'Has invitado a {guild_member.display_name}.')
