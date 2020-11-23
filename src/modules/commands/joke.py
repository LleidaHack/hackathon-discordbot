import random

from src.modules.commands import BaseCommand


class JokeCommand(BaseCommand):

    async def apply(self):
        import src.texts.jokes_texts as texts
        response = random.choice(texts.jokes)
        await self.ctx.channel.send(response)
