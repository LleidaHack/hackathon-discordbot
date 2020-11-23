from abc import ABC, abstractmethod

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
