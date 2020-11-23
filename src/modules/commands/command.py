import logging
from abc import ABC, abstractmethod
from functools import wraps

from discord.ext.commands import Context

from src.crud.firebase import Firebase


class BaseCommand(ABC):

    def __init__(self, context: Context):
        if not type(context) is Context:
            raise Exception
        self.ctx = context

    @abstractmethod
    async def apply(self):
        pass


class FireBaseCommand(BaseCommand, ABC):

    def __init__(self, context: Context, database: Firebase):
        super().__init__(context)
        self.DB = database

    @staticmethod
    def authorization_required(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            import src.texts.auth as txt
            command = args[0]
            ctx = args[1]
            user = command.DB.get_user(discord_id=ctx.message.author.id)
            if user is None:
                logging.info("Usuario no registrado")
                await ctx.send(txt.NOT_REGISTERED_ERROR)
                return
            logging.info(f"Usuario registrado")
            return await func(*args)
        return wrapper
