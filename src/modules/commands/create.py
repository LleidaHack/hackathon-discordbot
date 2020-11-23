from discord import User, Guild, Member
from discord.ext.commands import Context

import src.texts.create_texts as texts
from src.crud.firebase import Firebase
from src.models.group import Group
from src.modules.commands import FireBaseCommand
from src.modules.utils import GroupCreator


class CreateCommand(FireBaseCommand):

    def __init__(self, context: Context, database: Firebase, user: User, group_creator: GroupCreator):
        super().__init__(context, database)
        self.member = self.ctx.guild.get_member(user.id)
        self.group_name = None
        self.group_creator = group_creator

    async def apply(self):
        msg = self.ctx.message.content.split()
        if len(msg) < 2:
            await self.ctx.send(texts.SINTAXIS_ERROR)
            return
        self.group_name = ' '.join(msg[1:])
        if self.group_exists():
            await self.ctx.send(texts.GROUP_ALREADY_EXISTS_ERROR)
            return
        await self.ctx.send(texts.STARTING_CREATE_GROUP)
        firebase_user = self.DB.get_user(discord_id=self.member.id)
        await self.group_creator.create_group(Group(name=self.group_name), self.member, firebase_user)
        await self.ctx.send(texts.CREATED_GROUP)

    def group_exists(self):
        return self.DB.recover_web_group(self.group_name) is not None or \
               self.DB.get_group(self.group_name) is not None
