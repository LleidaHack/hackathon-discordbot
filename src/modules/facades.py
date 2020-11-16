from typing import Union

from discord import User as DiscordUser
from discord import Member
from discord.ext.commands import Context


class ContextFacade:

    def __init__(self, ctx):
        self.__ctx: Context = ctx

    def get_message(self) -> str:
        return self.__ctx.message.content

    def get_author(self) -> Union[Member, DiscordUser]:
        return self.__ctx.author
