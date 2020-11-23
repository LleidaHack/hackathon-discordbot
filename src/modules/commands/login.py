from discord import User
from discord.ext.commands import Context

import src.texts.login_text as login_texts
from src.crud.firebase import Firebase
from src.modules.commands import FireBaseCommand
from src.modules.login import StartLogin
from src.modules.pools.authentication import AuthenticationPool


class LoginCommand(FireBaseCommand):

    def __init__(self, context: Context, database: Firebase, author: User, pool: AuthenticationPool):
        super().__init__(context, database)
        self.author = author
        self.pool = pool

    async def apply(self):
        if self.is_on_guild():
            await self.ctx.send(login_texts.PM_SENDED)
        await StartLogin(self.DB, self.pool).start_login(self.author)

    def is_on_guild(self) -> bool:
        return self.ctx and self.ctx.guild
