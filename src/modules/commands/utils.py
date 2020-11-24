import traceback
from abc import ABC
from functools import wraps

import discord
from discord import Guild, TextChannel


class CatchedError(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


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
                channel: TextChannel = guild.get_channel(780723137968472075)
                async with channel.typing():
                    mod_role = filter(lambda x: x.name == 'LleidaHacker', guild.roles).__next__()
                    await channel.send(mod_role.mention)
                    embed = discord.Embed(title='¡Error! :eye::lips::eye:')
                    value = ''.join(traceback.format_exception(None, e, e.__traceback__))
                    embed.add_field(name='Información',
                                    value=f'Función *{func.__name__}* of {args[0].__class__.__name__}\nFrame:\n {e.__traceback__.tb_frame}',
                                    inline=False)
                    embed.add_field(name='Traceback', value=f'```{value}```',
                                    inline=False)
                    await channel.send(embed=embed)
                raise CatchedError
        return wrapper

