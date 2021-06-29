import logging
import discord
from discord import embeds 
import os

from src.modules.commands import BaseCommand
from src.modules.commands.utils import TraceCommand


class InfoCommand(BaseCommand):

    @TraceCommand.traceback_print
    async def apply(self):
        import src.texts.help_texts as texts
        from src.texts.const import const 
        logging.info("Enviando mensaje de información")
        bot_info_channel_id = int(os.getenv('INFO_BOT_CHANNEL_ID'))
        channel = self.ctx.guild.get_channel(bot_info_channel_id)

        embed = discord.Embed(
            colour=discord.Colour.blue(),
            title=f"{const.EVENT_NAME} {const.EVENT_YEAR}" ,
            description=texts.START_DESCRIPTION_MESSAGE
        )
        embed.add_field(name=f'{const.COMMAND_PREFIX}help',value=texts.HELP_COMMAND, inline=False)
        embed.add_field(name=f'{const.COMMAND_PREFIX}login',value=texts.LOGIN_COMMAND, inline=False)
        embed.add_field(name=f'{const.COMMAND_PREFIX}create <team_name>',value=texts.CREATE_COMMAND, inline=False)
        embed.add_field(name=f'{const.COMMAND_PREFIX}invite <discord_user>',value=texts.INVITE_COMMAND, inline=False)
        embed.add_field(name=f'{const.COMMAND_PREFIX}join <team_name>',value=texts.JOIN_COMMAND, inline=False)
        embed.add_field(name=f'{const.COMMAND_PREFIX}leave',value=texts.LEAVE_COMMAND, inline=False)
        embed.add_field(name=f'{const.COMMAND_PREFIX}ask <question>',value=texts.ASK_COMMAND, inline=False)
        embed.add_field(name=f'{const.COMMAND_PREFIX}joke',value=texts.JOKE_COMMAND, inline=False)
        embed.add_field(name=f'{const.COMMAND_PREFIX}rpsls',value=texts.RPSLS_COMMAND, inline=False)

        await channel.send(embed=embed)
