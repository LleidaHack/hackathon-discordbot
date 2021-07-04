import logging
from src.modules.commands.command import BaseCommand
from discord import User, user
from discord.ext.commands import Context

import src.texts.register_texts as register_texts
from src.crud.firebase import BotDatabase, WebDatabase
from src.modules.commands.utils import TraceCommand
from src.modules.login import StartLogin
from src.modules.pools.authentication import AuthenticationPool
class RegisterCommand(BaseCommand):

    def __init__(self, context: Context, database: WebDatabase):
        super().__init__(context)
        self.webDB = database
        self.user_info = self.ctx.message.content.split(' ')[1:]

    @TraceCommand.traceback_print
    async def apply(self):
        if len(self.user_info)>= 3:
            mail = self.user_info[0]
            name = self.user_info[1]
            last_name = self.user_info[2]
            github = self.user_info[3] if len(self.user_info) > 3 else ''
            nickname = self.user_info[4] if len(self.user_info) > 4 else ''
        else:
            logging.warn('Se ha solicitado crear un usuario, pero no se ha introducido bien el comando. INTRODUCIDO:' + self.ctx.message.content)
            await self.ctx.send(register_texts.COMMAND_HELP_USAGE)
            return
        if not self.webDB.recover_web_user(mail):
            self.webDB.register_user(mail, name, last_name, github, nickname)
            await self.ctx.send(register_texts.COMMAND_USER_CREATED)
        else: 
            await self.ctx.send(register_texts.COMMAND_USER_ALREADY_EXISTS)

