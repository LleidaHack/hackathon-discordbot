import random
import logging
import discord

from src.modules.commands import BaseCommand
from src.modules.commands.utils import TraceCommand


class BroadcastCommand(BaseCommand):

    def __init__(self, ctx, category_id):
        super().__init__(ctx)
        self.category_id = category_id

    @TraceCommand.traceback_print
    async def apply(self):
        msg = self.ctx.message
        if msg.reference is None:
            self.ctx.send('Oye! Me falta que referencies el mensaje')
            return
        msg_cont = await self.ctx.fetch_message(msg.reference.message_id)
        category = discord.utils.get(self.ctx.guild.categories, id=int(self.category_id))
        for channel in category.channels:
            logging.info(f'channel {channel}')
            await channel.send(msg_cont.content)
        return
        