from discord import User
from discord.ext.commands import Context
from src.crud.firebase import Firebase
from src.modules.commands import FireBaseCommand
import src.texts.create_texts as texts
from src.models.group import Group
class CreateCommand(FireBaseCommand):

    def __init__(self, context: Context, database: Firebase, user: User, guild_id: int, group_creator: GroupCreator):
        super().__init__(context, database)
        self.member = user
        if not context.guild:
            ctx.guild = self.client.get_guild(guild_id)
            self.member = context.guild.get_member(user.id)
        self.group_name = None
        self.group_creator = group_creator

    def apply(self):
        msg = self.ctx.message.content.split()
        if len(msg) > 1:
            self.group_name = msg[1:]


    async def create(self):
        if not self.group_name:
            await self.context.send(texts.SINTAXIS_ERROR)
            return
        if self.group_exists():
            await self.context.send(texts.GROUP_ALREADY_EXISTS_ERROR)
            return

        await self.context.send(texts.STARTING_CREATE_GROUP)
        group = Group(name=self.group_name)
        await self.group_creator.create_group(self.group_name, self.member)
        await self.context.send(texts.CREATED_GROUP)
        return
    def group_exists(self):
        return self.DB.recover_web_group(name=self.group_name) is not None or self.DB.get_group(name=self.group_name) is not None