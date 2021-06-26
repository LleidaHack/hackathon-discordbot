import asyncio
import logging

from discord import User

import src.texts.login_text as login_texts
from src.crud.firebase import Firebase
from src.modules.pools.authentication import AuthenticationPool


class StartLogin:
    def __init__(self, database: Firebase, pool: AuthenticationPool):
        self.database = database
        self.pool = pool

    async def start_login(self, author: User):
        if not self.can_login(author):
            logging.info("Usuario " + str(author) + "ya conectado")
            await author.send(login_texts.REGISTER_YOU_ARE_LOGGED)
            return
        self.pool.add_newbie(author)
        logging.info("Enviando mensaje de inicio de registro a " + str(author))
        await author.send(login_texts.REGISTER_MESSAGE)

    def can_login(self, author: User):
        return not self.database.get_user(discord_id=author.id)
