from discord import User
from discord.ext.commands import Context
from src.crud.firebase import Firebase
from src.modules.commands import FireBaseCommand
import src.texts.create_texts as texts
from src.models.group import Group
class CreateCommand(FireBaseCommand):

    def __init__(self, context: Context, database: Firebase, user: User, guild_id: int):
        super().__init__(context, database)
        self.author = user
        if not context.guild:
            ctx.guild = self.client.get_guild(guild_id)
            self.author = context.guild.get_member(user.id)
        self.group_name = None

    def apply(self):
        msg = self.ctx.message.content.split()
        if len(msg) > 1:
            self.group_name = msg[1:]


    async def create(self):
        if not self.group_name:
            await self.context.send(texts.GROUP_ALREADY_EXISTS_ERROR)
            return
        group = Group(name=self.group_name)
        