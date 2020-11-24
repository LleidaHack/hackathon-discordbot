import logging
import re

from discord.ext.commands import Context

from src.modules.commands import BaseCommand
from src.modules.commands.utils import TraceCommand
from src.modules.pools.questions import QuestionPool


class AskCommand(BaseCommand):

    def __init__(self, context: Context, pool: QuestionPool, client):
        super().__init__(context)
        self.client = client
        self.pool = pool
        self.question = self.ctx.message.content[7:]

    @TraceCommand.traceback_print
    async def apply(self):
        import src.texts.ask_reply_texts as ask_texts
        if self.question != '':
            logging.info("Enviando pregunta")
            await self.ctx.author.send(embed=ask_texts.EMBED_ASK_MESSAGE)
            channelId = AskCommand.get_channel_id(self.ctx, 'preguntas_participantes')
            channel = self.client.get_channel(channelId)
            self.pool.add_question(self.ctx.author, self.question)
            await channel.send(embed=ask_texts.SEND_TO_ADMINS(str(self.pool.get_last_question()), str(self.ctx.author), self.question))
        else:
            await self.ctx.author.send(ask_texts.EMBED_VOID_MESSAGE)

    @staticmethod
    def get_channel_id(ctx, name=None):
        for channel in ctx.guild.channels:
            if channel.name == name:
                return channel.id


class ReplyCommand(BaseCommand):

    def __init__(self, context: Context, pool: QuestionPool, num: str):
        super().__init__(context)
        self.pool: QuestionPool = pool
        self.num_question: int = int(num)
        self.reply: str = self.__get_reply_from_context()

    @TraceCommand.traceback_print
    async def apply(self):
        import src.texts.ask_reply_texts as ask_texts
        await self.pool.get_author(self.num_question).send(embed=ask_texts.REPLY_TO_USER(str(self.ctx.author),self.pool.get_question(self.num_question),self.reply))
        self.pool.remove_answered_question(self.num_question)

    def __get_reply_from_context(self):
        all_comand: str = self.ctx.message.content
        count_of_words = 0
        for i in range(len(all_comand)):
            if all_comand[i] == ' ':
                count_of_words += 1
            if count_of_words == 2:
                break
        return all_comand[i:]