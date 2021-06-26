import logging
from typing import Optional, List

import discord
from discord import Guild, Member
from discord.ext.commands import Context

from src.crud.firebase import Firebase
from src.models.group import Group
from src.modules.commands import FireBaseCommand
from src.models.user import User as ModelUser
from src.modules.commands.utils import TraceCommand


class LeaveCommand(FireBaseCommand):
    def __init__(self, context: Context, database: Firebase):
        super().__init__(context, database)

    @TraceCommand.traceback_print
    @FireBaseCommand.authorization_required
    @FireBaseCommand.group_required
    async def apply(self):
        from src.modules.facades import ContextFacade
        import src.texts.leave_texts as txt
        fac: ContextFacade = ContextFacade(self.ctx)
        logging.info(f"leave command por {fac.get_author().name}")
        user: ModelUser = self.DB.get_user_from_id(fac.get_author().id)
        group = self.DB.get_group(user.group_name)
        if not group:
            logging.error(f"No se ha encontrado el grupo {user.group_name} del usuario {user.get_full_name()}.")
            await self.ctx.send(txt.SERVER_ERROR)
            return
        self.remove_user_from_group(user, group)
        role = discord.utils.get(self.ctx.guild.roles, name=group.name)
        member = self.ctx.guild.get_member(user.discord_id)
        await member.remove_roles(role)
        if group.size() == 0:
            await self.remove_group_chanels(role)
            await self.remove_empty_group(group, role)
        await self.ctx.send(txt.LEAVE_MSG(member.name, role.name))

    def remove_user_from_group(self, user, group):
        group.remove_user(user.discord_id)
        user.group_name = None
        self.DB.create_or_update_user(user)
        self.DB.create_or_update_group(group)

    async def remove_empty_group(self, group, role):
        self.DB.delete_group(group.name)
        await role.delete()
        
    async def remove_group_chanels(self, role):        
        chanels = list(filter(lambda x: role in x.overwrites, self.ctx.guild.channels))
        # if the channel exists
        for chanel in chanels:
            logging.error(f"Deleting Chanel")
            await chanel.delete()
        