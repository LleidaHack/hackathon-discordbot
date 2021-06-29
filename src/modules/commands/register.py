from src.modules.commands import FireBaseCommand
from src.crud.firebase import BotDatabase, WebDatabase

from discord.ext.commands import Context
class RegisterCommand(FireBaseCommand):
    def __init__(self, context: Context, database: BotDatabase):
        super().__init__(context, database)

    async def apply():
        pass