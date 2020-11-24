import logging
from typing import Optional, List

import discord
from discord import User as DiscordUser, Member
from discord.ext.commands import Context
from src.models.invitation import Invitation
import src.texts.join_texts as txt
from src.crud.firebase import Firebase
from src.models.group import Group
from src.models.user import User as ModelUser
from src.modules.commands import FireBaseCommand
from src.modules.commands.command import CommandError
from src.modules.utils import GroupCreator

class JoinCommand(FireBaseCommand):

    def __init__(self, context: Context, database: Firebase):
        super().__init__(context, database)

    @FireBaseCommand.authorization_required
    @FireBaseCommand.non_group_required
    async def apply(self):
        invitations : list = list(map(lambda x: x if x[1].is_pending() else None, self.DB.get_invitations(self.ctx.author.id)))
        if not any(invitations):
            await self.ctx.send(txt.ANY_INVITE(self.ctx.author.name, self.ctx.author.discriminator))
            return
        msg = self.ctx.message.content.split()
        if len(msg) <= 1 and len(invitations) > 1:
            await self.ctx.send(txt.MANY_INVITES(list(map(lambda x: x[1].group_name, invitations))))
            return
        inv_id, invitation = self.DB.get_invitation(self.ctx.author.id, ' '.join(msg[1:])) if len(msg) > 1 else invitations[0]
        await self.accept_invitation(invitation)


    async def accept_invitation(self, invitation: Invitation):
        user, group, member, role = await self.recover_entities(invitation.user_id, invitation.group_name)
        logging.info(f"Añadiendo el rol a miembro {member.name} al grupo {invitation.group_name}")
        group.add_user(self.ctx.author.id)
        if not self.DB.accept_invitation(invitation.user_id, invitation.group_name):
            await self.ctx.send(txt.INVITATION_LOST)
            return
        logging.info(f"Aceptación de invitación correcto. Uniendo a roles y actualizando Bases de datos")
        
        await member.add_roles(role)
        self.DB.create_or_update_user(user)
        self.DB.create_or_update_group(group)

        await self.ctx.send(txt.MEMBER_REGISTERED_IN(member.name, role.name))

    async def recover_entities(self, user_id: int, group_name: str):
        user = self.DB.get_user_from_id(user_id)
        user.group_name = group_name
        group = self.DB.get_group(group_name)
        if not group:
            await self.ctx.send(txt.GROUP_LOST(group_name))
            return
        member = self.ctx.guild.get_member(self.ctx.author.id)
        role = discord.utils.get(self.ctx.guild.roles, name=group_name)
        return user, group, member, role