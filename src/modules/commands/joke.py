import random

import discord

from src.modules.commands import BaseCommand
from src.modules.commands.utils import TraceCommand


class JokeCommand(BaseCommand):

    @TraceCommand.traceback_print
    async def apply(self):
        import src.texts.jokes_texts as texts
        joke = random.choice(texts.jokes)
        response = random.choice(texts.response)
        await self.ctx.channel.send(response)
        await self.ctx.channel.send(f'```{joke}```')
