import logging

from src.modules.commands import BaseCommand


class HelpCommand(BaseCommand):

    async def apply(self):
        import src.texts.help_texts as texts
        logging.info("Enviando mensaje de ayuda")
        await self.ctx.send(texts.GLOBAL_HELP_MESSAGE, delete_after=20)
        await self.ctx.author.send(embed=texts.EMBED_HELP_MESSAGE)
