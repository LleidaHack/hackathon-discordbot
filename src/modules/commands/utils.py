import io
import traceback
from abc import ABC
from functools import wraps
import logging
import os
import toml
config = toml.load('config.toml')
import discord
from discord import Guild, TextChannel, File


class CatchedError(Exception):

    def __init__(self, *args: object, original=None) -> None:
        super().__init__(*args)
        self.original=original


class TraceCommand(ABC):

    @staticmethod
    def traceback_print(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            """import src.texts.auth as txt
            command = args[0]
            ctx = command.ctx"""
            try:
                value = await func(*args)
                return value
            except Exception as e:
                command = args[0]
                guild: Guild = command.ctx.guild
                channel: TextChannel = guild.get_channel(config['LOG_ERROR_CHANNEL_ID'])
                async with channel.typing():
                    mod_role = filter(lambda x: x.name == config['ADMIN_ROLE'], guild.roles).__next__()
                    embed = discord.Embed(title='¡Error! :eye::lips::eye:')
                    value = ''.join(traceback.format_exception(None, e, e.__traceback__))
                    logging.error(value)
                    embed.add_field(name='Información',
                                    value=f'**Función** *{func.__name__}* of {args[0].__class__.__name__}'
                                          f'\n **User**: {command.ctx.author}\n '
                                          f'**Command**: {command.ctx.message.content}',
                                    inline=False)
                    await channel.send(mod_role.mention, embed=embed, file=File(io.StringIO(value), filename='error.txt'))
                raise CatchedError(e)
        return wrapper

