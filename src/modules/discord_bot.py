#!/usr/bin/python3
import logging
import os

import discord
from crud.firebase import Firebase
from discord.ext import commands as discord_commands
from discord.ext.commands import Context
from models.team import Team


class DB:
    __database = Firebase()

    @staticmethod
    def get() -> Firebase:
        return DB.__database


class DiscordBot:
    def __init__(self):
        logging.info("Reading bot config data")

        intents = discord.Intents.all()
        self.client = discord_commands.Bot(os.getenv('DISCORD_PREFIX'), guild_subscriptions=True, intents=intents)
        self.token = os.getenv('DISCORD_TOKEN')
        self.index = 0
        self.client.remove_command('help')
        logging.info("Reading bot functions")

        self.questions = {}

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
        async def invite(ctx):
            await self.invite_command(ctx)

        self.question_num = 0

        @self.client.event
        async def on_member_join(member):
            await self.login(member)

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

        user = DB.get().getUser(discord_id=ctx.message.author.id)
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
        group = DB.get().getGroup(group_name=' '.join(command[1:]))
        if not group:
            group = DB.get().recoverWebGroup(' '.join(command[1:]))
        if group:
            logging.info("[COMMAND CREATE - ERROR] El grupo indicado ya existe")
            await ctx.send(texts.GROUP_ALREADY_EXISTS_ERROR)
            return
        await ctx.send(texts.STARTING_CREATE_GROUP)
        group = Team(' '.join(command[1:]), [ctx.message.author.id])
        logging.info("[COMMAND CREATE - OK] Solicitando creacion de grupo")
        DB.get().createOrUpdateGroup(group)
        guild = ctx.guild
        logging.info("[COMMAND CREATE - OK] Creando rol")

        await guild.create_role(name=group.name)
        role = discord.utils.get(ctx.guild.roles, name=group.name)
        logging.info("[COMMAND CREATE - OK] Añadiendo el usuario al rol")
        await ctx.message.author.add_roles(role)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            role: discord.PermissionOverwrite(read_messages=True)
        }
        logging.info("[COMMAND CREATE - OK] Localizando categoria de equipos")

        for cat in guild.categories:
            if str(cat.id) == os.getenv('TEAMS_CATEGORY_ID'):
                logging.info("[COMMAND CREATE - OK] Creando canales de chat y voz")
                await guild.create_text_channel(group.name, overwrites=overwrites, category=cat)
                await guild.create_voice_channel(group.name, overwrites=overwrites, category=cat)
                break

        logging.info("[COMMAND CREATE - OK] Informando all Ok")
        await ctx.send(texts.CREATED_GROUP)

        pass

    async def ask_command(self, ctx, question):
        import texts.ask_texts as ask_texts
        logging.info("Enviando pregunta")
        await ctx.author.send(embed=ask_texts.EMBED_ASK_MESSAGE)
        channelId = DiscordBot.get_channel_id(ctx, 'preguntas_participantes')
        channel = self.client.get_channel(channelId)
        self.questions[self.question_num] = ctx.author
        print(self.questions)
        await channel.send('#' + str(self.question_num) + '  >  ' + question)
        self.question_num += 1

    async def reply_command(self, ctx, num, reply):
        await self.questions[int(num)].send('La respuesta a tu pregunta fue:  ' + reply)

    @staticmethod
    def get_channel_id(ctx, name=None):
        for channel in ctx.guild.channels:
            if channel.name == name:
                return channel.id

    async def login(self, member):
        import texts.login_text as login_texts
        logging.info("Enviando mensaje por privado para hacer login")
        name = member.nick
        await member.send(login_texts.send_message_login(name), delete_after=20)
        await member.author.send(embed=login_texts.EMBED_LOGIN_MESSAGE)

    def invite_command(self, ctx: Context):
        from texts.invite_texts as txt
        username = {ctx.author.name}
        logging.info(f"Comando 'invite' recibido por usuario {username}")
        team: Team = DB.get().getGroup(DB.get().getUser(ctx.author.id).group_name)
        if not team:
            logging.error(f"{ctx.author.name} no tiene grupo")
            await ctx.send(txt.NOT_IN_GROUP)
            return
        people = list(map(lambda x: x.split('#'), ctx.message.content.split()[1:]))
        if any(people):
            logging.error("Gente no encontrada.")
            await ctx.send(txt.NOT_FOUND_PEOPLE)
            return
        people = list(map(lambda x: DB.get().getUser(username=x[0], discriminator=x[1]), people))
        logging.info(f"Gente encontrada: {[p.name for p in people]}")
        if team.size() + len(people) < 4:
            logging.error(
                f"Usuario {username} quiere añadir al grupo {team.name} {len(people)} personas pero ya son {team.size()}")
            await ctx.send(txt.TEAM_OVERFLOW)
            return
        guild = ctx.guild
        role = discord.utils.get(guild.roles, name=team.name)
        if not role:
            logging.error(f"Not found role {team.name}")
            return
        for p in people:
            team.add_user(p)
            member = guild.get_member(p.discord_id)
            logging.info(f"Añadiendo el rol {role.name} al miembro {member.name}")
            await member.add_roles(role)
            await ctx.send(f"¡{member.name} añadido al grupo {role.name}!")

