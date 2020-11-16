#!/usr/bin/python3
import logging
import os

import discord
from discord.ext import commands as discord_commands

from crud.firebase import Firebase
from models.team import Team
from models.user import User

class DiscordBot:
    def __init__(self):
        logging.info("Reading bot config data")
        intents = discord.Intents.all()

        self.client = discord_commands.Bot(os.getenv('DISCORD_PREFIX'), guild_subscriptions=True, intents=intents)
        self.token = os.getenv('DISCORD_TOKEN')
        self.index = 0
        self.client.remove_command('help')
        self.database = Firebase()
        logging.info("Reading bot functions")

        self.questions = {}
        self.question_num = 0
        self.user_registering = {}
        @self.client.command()
        async def help(ctx):
            await self.help_command(ctx)

        @self.client.command()
        async def ask(ctx, question):
            await self.ask_command(ctx, question)

        @self.client.command()
        async def reply(ctx, num, reply):
            await self.reply_command(ctx, num, reply)

        @self.client.command()
        async def create(ctx):
            await self.create_command(ctx)

        @self.client.command()
        async def register(ctx):
            await self.start_register(ctx.author)

        @self.client.event
        async def on_member_join(member):
            import texts.login_text as login_texts

            await member.send(embed=login_texts.WELCOME_MESSAGE)
            await self.start_register(member)

        @self.client.listen('on_message')
        async def on_message(message):
            if message.author in self.user_registering and not message.guild and not message.author.bot:
                logging.info("Email enviado")
                await self.login(message.author, message.content)
                logging.info("Email checked")
                

    def start(self):
        logging.info("Starting bot!")
        self.client.run(self.token)



    async def help_command(self, ctx):
        import texts.help_texts as texts

        logging.info("Enviando mensaje de ayuda")
        await ctx.send(texts.GLOBAL_HELP_MESSAGE, delete_after=20)
        await ctx.author.send(embed=texts.EMBED_HELP_MESSAGE)

    async def create_command(self, ctx):
        import texts.create_texts as texts

        user = self.database.getUser(discord_id=ctx.message.author.id)
        if not user:
            logging.info("[COMMAND CREATE - ERROR] Usuario no registrado")
            await ctx.send(texts.NOT_REGISTERED_ERROR)
            return
        if user.group_name is not None or user.group_name != '':
            logging.info("[COMMAND CREATE - ERROR] El usuario ya se encuentra en un grupo")
            await ctx.send(texts.ALREADY_ON_GROUP_ERROR)
            return
        command = ctx.message.content.split()
        if len(command) < 2:
            logging.info("[COMMAND CREATE - ERROR] La sintaxis es incorrecta")
            await ctx.send(texts.SINTAXIX_ERROR)
            return
        group = self.database.getGroup(group_name=' '.join(command[1:]))
        if not group:
            group = self.database.recoverWebGroup(' '.join(command[1:]))
        if group:
            logging.info("[COMMAND CREATE - ERROR] El grupo indicado ya existe")
            await ctx.send(texts.GROUP_ALREADY_EXISTS_ERROR)
            return
        await ctx.send(texts.STARTING_CREATE_GROUP)
        group = Team(' '.join(command[1:]), [ctx.message.author.id])
        logging.info("[COMMAND CREATE - OK] Solicitando creacion de grupo")
        self.database.createOrUpdateGroup(group)

        role = await  self.create_group_on_server(ctx.guild, group)


        logging.info("[COMMAND CREATE - OK] Añadiendo el usuario al rol")
        await ctx.message.author.add_roles(role)
        logging.info("[COMMAND CREATE - OK] Informando all Ok")
        await ctx.send(texts.CREATED_GROUP)

    async def create_group_on_server(self, guild, group):
        await guild.create_role(name=group.group_name)
        role = discord.utils.get(guild.roles, name=group.group_name)
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            role: discord.PermissionOverwrite(read_messages=True)
        }
        logging.info("[CREATE GROUP - OK] Localizando categoria de equipos")

        for cat in guild.categories:
            if str(cat.id) == os.getenv('TEAMS_CATEGORY_ID'):
                logging.info("[CREATE GROUP - OK] Creando canales de chat y voz")
                await guild.create_text_channel(group.group_name, overwrites=overwrites, category=cat)
                await guild.create_voice_channel(group.group_name, overwrites=overwrites, category=cat)
                break

        return role

    async def ask_command(self,ctx,question):
        import texts.ask_reply_texts as texts
        logging.info("Enviando pregunta")
        question=' '.join(str(i) for i in question)
        await ctx.author.send(embed=texts.EMBED_ASK_MESSAGE)
        channelId=DiscordBot.get_channel_id(ctx,'preguntas_participantes')
        channel = self.client.get_channel(channelId)
        self.questions[self.question_num]=(ctx.author,question)
        await channel.send('#'+str(self.question_num)+'  >  '+question)
        self.question_num+=1

    async def reply_command(self,ctx,num,reply):
        import texts.ask_reply_texts as texts
        #TODO:check question existnce
        print(type(int))
        if (not str(num).isdigit()) or (not int(num) in self.questions.keys()):
            await ctx.send(embed=texts.REPLY_INDEX_ERR)
        reply=' '.join(str(i) for i in reply)
        msg = discord.Embed(title="Tu resspuesta ha llegado", color=0x00ff00)
        msg.add_field(name="Pregunta", value=self.questions[int(num)][1], inline=False)
        msg.add_field(name="Respuesta", value=reply, inline=False)
        # await self.questions[int(num)][0].send('La respuesta a tu pregunta fue:  '+reply)
        await self.questions[int(num)][0].send(embed=msg)
        del self.questions[int(num)]#a revisar porque puedes darle quizas 2 respuestas

    @staticmethod
    def get_channel_id(ctx, name=None):
        for channel in ctx.guild.channels:
            if channel.name == name:
                return channel.id

    async def start_register(self, author):
        import texts.login_text as login_texts
        user_discord = self.database.getUser(discord_id=author.id)
        if not user_discord:
            logging.info("Enviando mensaje de inicio de registro a " + str(author))

            await author.send(login_texts.REGISTER_MESSAGE)
            self.user_registering[author] = 0
        else:
            #send message already registrado
            pass
    async def login(self, user, email):
        import texts.login_text as login_texts
        logging.info("Email test")
        web_user, group = self.database.recoverWebGroupByUser(email)
        if web_user:
            logging.info("Usuario localizado")
            discord_user = self.database.getUser(email=email)
            if discord_user:
                await user.send(login_texts.REGISTER_ALREADY_REGISTER)
                pass
            else:
                guild = self.client.get_guild(int(os.getenv('GUILD')))
                member = guild.get_member(user.id)
                if guild:
                    if group:
                        discord_group = self.database.getGroup(group.group_name)
                        if not discord_group:
                            await  self.create_group_on_server(guild, group)
                            discord_group = group

                        role = discord.utils.get(guild.roles, name=group.group_name)
                        discord_group.members.append(user.id)
                        self.database.createOrUpdateGroup(discord_group)
                        discord_user = User(user.name, user.discriminator, user.id, group.group_name,email)
                        logging.info("[REGISTER - OK] Añadiendo el usuario al rol")
                        await member.add_roles(role)
                        await user.send(login_texts.USER_HAS_GROUP)

                    else:
                        discord_user = User(user.name, user.discriminator, user.id, '', email)
                        await user.send(login_texts.USER_NO_GROUP)


                    self.database.createOrUpdateUser(discord_user)
                    # Creacion usuario
                    await user.send(login_texts.REGISTER_OK)
                else:
                    print("ERROR CONFIG")
                    print(os.getenv('GUILD'))
        else:
            logging.info("No se ha encontrado al usuario")
            await user.send(login_texts.REGISTER_KO)

            pass
