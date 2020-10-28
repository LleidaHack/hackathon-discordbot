#!/usr/bin/python3
import logging, os
import discord
from discord.ext import commands as discord_commands, tasks
# from discord.ext import commands as discord_commands
import texts.help_texts as help_texts
import texts.ask_texts as ask_texts
class DiscordBot:
    def __init__(self):
        logging.info("Reading bot config data")
        self.client = discord_commands.Bot(os.getenv('DISCORD_PREFIX'))
        self.token = os.getenv('DISCORD_TOKEN')
        self.index = 0
        self.client.remove_command('help')
        self.question_num=0
        self.questions={}
        @self.client.command()
        async def help(ctx):
            await self.help_command(ctx)
        @self.client.command()
        async def ask(ctx,question):
            await self.ask_command(ctx,question)
        @self.client.command()
        async def reply(ctx,num,reply):
            await self.reply_command(ctx,num,reply)
        pass

    def start(self):
        logging.info("Starting bot!")
        self.client.run(self.token)


    async def help_command(self, ctx):
        logging.info("Enviando mensaje de ayuda")

        await ctx.send(help_texts.GLOBAL_HELP_MESSAGE, delete_after=20)
        await ctx.author.send(embed=help_texts.EMBED_HELP_MESSAGE)
    
    async def ask_command(self,ctx,question):
        logging.info("Enviando pregunta")
        await ctx.author.send(embed=ask_texts.EMBED_ASK_MESSAGE)
        channelId=DiscordBot.get_channel_id(ctx,'preguntas_participantes')
        channel = self.client.get_channel(channelId)
        self.questions[self.question_num]=(ctx.author,question)
        await channel.send('#'+str(self.question_num)+'  >  '+question)
        self.question_num+=1

    async def reply_command(self,ctx,num,reply):
        #TODO:check question existnce
        msg = discord.Embed(title="Tu resspuesta ha llegado", color=0x00ff00)
        msg.add_field(name="Pregunta", value=self.questions[int(num)][1], inline=False)
        msg.add_field(name="Respuesta", value="hi2", inline=False)
        # await self.questions[int(num)][0].send('La respuesta a tu pregunta fue:  '+reply)
        await self.questions[int(num)][0].send(embed=msg)
        del self.questions[int(num)]#a revisar porque puedes darle quizas 2 respuestas

    @staticmethod
    def get_channel_id(ctx,name=None):
        for channel in ctx.guild.channels:
            if channel.name == name:
                return channel.id