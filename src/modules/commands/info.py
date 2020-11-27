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
        logging.info("Enviando mensaje de información")
        bot_info_channel_id = int(os.getenv('INFO_BOT_CHANNEL_ID'))
        channel = self.ctx.guild.get_channel(bot_info_channel_id)

        embed = discord.Embed(
            colour=discord.Colour.blue(),
            title="HackEPS 2020",
            description=texts.START_DESCRIPTION_MESSAGE
        )
        embed.add_field(name='eps!help',value=texts.HELP_COMMAND, inline=False)
        embed.add_field(name='eps!login',value=texts.LOGIN_COMMAND, inline=False)
        embed.add_field(name='eps!create <team_name>',value=texts.CREATE_COMMAND, inline=False)
        embed.add_field(name='eps!invite <discord_user>',value=texts.INVITE_COMMAND, inline=False)
        embed.add_field(name='eps!join <team_name>',value=texts.JOIN_COMMAND, inline=False)
        embed.add_field(name='eps!leave',value=texts.LEAVE_COMMAND, inline=False)
        embed.add_field(name='eps!ask <question>',value=texts.ASK_COMMAND, inline=False)
        embed.add_field(name='eps!joke',value=texts.JOKE_COMMAND, inline=False)
        embed.add_field(name='eps!rpsls',value=texts.RPSLS_COMMAND, inline=False)

        await channel.send(embed=embed)
