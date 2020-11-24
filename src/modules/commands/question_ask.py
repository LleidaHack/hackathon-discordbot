import logging

from discord.ext.commands import Context

from src.modules.commands import BaseCommand
from src.modules.commands.utils import TraceCommand
from src.modules.pools.questions import QuestionPool


class AskCommand(BaseCommand):

    def __init__(self, context: Context, question: str, pool: QuestionPool, client):
        super().__init__(context)
        self.client = client
        self.pool = pool
        self.question = question

    @TraceCommand.traceback_print
    async def apply(self):
        import src.texts.ask_reply_texts as ask_texts
        logging.info("Enviando pregunta")
        await self.ctx.author.send(embed=ask_texts.EMBED_ASK_MESSAGE)
        channelId = AskCommand.get_channel_id(self.ctx, 'preguntas_participantes')
        channel = self.client.get_channel(channelId)
        self.pool.add_question(self.ctx.author)
        await channel.send('#' + str(self.pool.get_last_question()) + '  >  ' + self.question)

    @staticmethod
    def get_channel_id(ctx, name=None):
        for channel in ctx.guild.channels:
            if channel.name == name:
                return channel.id


class ReplyCommand(BaseCommand):

    def __init__(self, context: Context, questions: QuestionPool, num: str, reply: str):
        super().__init__(context)
        self.questions: QuestionPool = questions
        self.num_question: int = int(num)
        self.reply: str = reply

    async def apply(self):
        await self.questions.get_author(self.num_question).send('La respuesta a tu pregunta fue:  ' + self.reply)
