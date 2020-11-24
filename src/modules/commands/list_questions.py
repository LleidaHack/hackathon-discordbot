import logging
import discord

from discord.ext.commands import Context

from src.modules.commands import BaseCommand
from src.modules.commands.utils import TraceCommand
from src.modules.pools.questions import QuestionPool


class ListQuestions(BaseCommand):

    def __init__(self, context: Context, pool : QuestionPool):
        super().__init__(context)
        self.pool = pool

    @TraceCommand.traceback_print
    async def apply(self):
        channel = self.ctx.channel
        if(str(channel) == "preguntas_participantes"):
            body = ""
            for question in self.pool.get_unanswered_questions().items():
                body += "#"+str(question[0])+" "+str(question[1]["author"])+": "+question[1]["question"]+"\n"
            await self.ctx.channel.send(embed = discord.Embed(
                colour = discord.Colour.blue(),
                title = "Listado Preguntas a Contestar:",
                description = body
            ))
        else:
            await self.ctx.author.send("Para ejecutar este comando lo tienes que hacer desde el canal preguntas_participantes")
