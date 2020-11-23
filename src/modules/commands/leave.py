import logging
from typing import Optional, List

import discord
from discord import Guild, Member
from discord.ext.commands import Context

from src.crud.firebase import Firebase
from src.models.group import Group
from src.modules.commands import FireBaseCommand
from src.models.user import User as ModelUser

class LeaveCommand(FireBaseCommand):
    def __init__(self, context: Context, database: Firebase):
        super().__init__(context, database)

    async def apply(self):
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
