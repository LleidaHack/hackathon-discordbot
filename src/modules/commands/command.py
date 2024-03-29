import logging
from abc import ABC, abstractmethod
from functools import wraps
from types import TracebackType
from typing import Optional

from discord.ext.commands import Context

from src.crud.firebase import BotDatabase, WebDatabase


class BaseCommand(ABC):

    def __init__(self, context: Context):
        self.ctx = context

    @abstractmethod
    async def apply(self):
        pass


class FireBaseCommand(BaseCommand, ABC):

    def __init__(self, context: Context, database: BotDatabase):
        super().__init__(context)
        self.DB = database

    @staticmethod
    def authorization_required(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            import src.texts.auth as txt
            command = args[0]
            ctx = command.ctx
            user = command.DB.get_user(discord_id=ctx.message.author.id)
            if user is None:
                logging.info("Usuario no registrado")
                await ctx.send(txt.NOT_REGISTERED_ERROR)
                return
            logging.info(f"Usuario registrado")
            return await func(*args)

        return wrapper

    @staticmethod
    def group_required(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            import src.texts.auth as txt
            command = args[0]
            ctx = command.ctx
            user = command.DB.get_user(discord_id=ctx.message.author.id)
            if user.group_name is None:
                logging.info("Usuario sin grupo")
                await ctx.send(txt.NOT_INGROUP_ERROR(ctx.author))
                return
            logging.info(f"Usuario con grupo")
            return await func(*args)

        return wrapper

    @staticmethod
    def non_group_required(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            import src.texts.auth as txt
            command = args[0]
            ctx = command.ctx
            user = command.DB.get_user(discord_id=ctx.message.author.id)
            if user.group_name is not None:
                logging.info("Usuario con grupo")
                await ctx.send(txt.ALREADY_ON_GROUP_ERROR)
                return
            logging.info(f"Usuario sin grupo")
            return await func(*args)

        return wrapper


class CommandError(BaseException):

    def __init__(self, *args: object, **kwargs) -> None:
        super().__init__(*args)
        if 'msg' in kwargs:
            self.msg = kwargs['msg']

    def __str__(self) -> str:
        return super().__str__() + f": {self.msg}"

    def __repr__(self) -> str:
        return super().__repr__()

    def with_traceback(self, tb: Optional[TracebackType]) -> BaseException:
        return super().with_traceback(tb)
