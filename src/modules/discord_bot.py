#!/usr/bin/python3
import logging
import os
from typing import List

import discord
from discord import Member
from discord.ext import commands as discord_commands
from discord.ext.commands import Context

from src.crud.firebase import Firebase
from src.models.invitation import Invitation
from src.models.team import Team
from src.models.user import User as ModelUser

DB = Firebase()


# at least:
# DB = lambda: Firebase()

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

        @self.client.command()
        async def join(ctx):
            await self.join_command(ctx)

        self.question_num = 0


        @self.client.command()
        async def login(ctx):
            await self.start_register(ctx.author)

        @self.client.event
        async def on_member_join(member):
            import src.texts.login_text as login_texts
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
        import src.texts.help_texts as texts

        logging.info("Enviando mensaje de ayuda")
        await ctx.send(texts.GLOBAL_HELP_MESSAGE, delete_after=20)
        await ctx.author.send(embed=texts.EMBED_HELP_MESSAGE)

    async def create_command(self, ctx):
        import src.texts.create_texts as texts

        user = DB.get_user(discord_id=ctx.message.author.id)
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
        group = DB.get_group(group_name=' '.join(command[1:]))
        if not group:
            group = DB.recover_web_group(' '.join(command[1:]))
        if group:
            logging.info("[COMMAND CREATE - ERROR] El grupo indicado ya existe")
            await ctx.send(texts.GROUP_ALREADY_EXISTS_ERROR)
            return
        await ctx.send(texts.STARTING_CREATE_GROUP)
        group = Team(' '.join(command[1:]), [ctx.message.author.id])
        logging.info("[COMMAND CREATE - OK] Solicitando creacion de grupo")
        DB.create_or_update_group(group)
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
        import src.texts.ask_texts as ask_texts
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

    async def invite_command(self, ctx: Context):
        import src.texts.invite_texts as txt
        from typing import Union
        username: str = ctx.author.name
        logging.info(f"Comando 'invite' recibido por usuario {username}")
        team: Union[Team, bool] = DB.get_group(DB.get_user(ctx.author.id).group_name)
        if not team:
            logging.error(f"{ctx.author.name} no tiene grupo")
            await ctx.send(txt.NOT_IN_GROUP)
            return
        people = list(map(lambda x: x.split('#'), ctx.message.content.split()[1:]))
        people: List[ModelUser] = list(map(lambda x: DB.get_user(username=x[0], discriminator=x[1]), people))
        if any(people):
            logging.error("Gente no encontrada.")
            await ctx.send(txt.NOT_FOUND_PEOPLE)
            return
        logging.info(f"Gente encontrada: {[p.username for p in people]}")
        if team.size() + len(people) < 4:
            logging.error(
                f"Usuario {username} quiere añadir al grupo {team.name} {len(people)} personas pero ya son {team.size()}")
            await ctx.send(txt.TEAM_OVERFLOW)
            return
        for already_member in filter(lambda x: x.group_name is not None, people):
            logging.info(f"{already_member} está ya en otro grupo: {already_member.group_name}")
            await ctx.send(txt.ALREADY_IN_A_GROUP(already_member.username, already_member.group_name))
        people = list(filter(lambda x: x.group_name is None, people))
        guild = ctx.guild
        role = discord.utils.get(guild.roles, name=team.name)
        if not role:
            logging.error(f"Not found role {team.name}")
            return
        for p in people:
            member: Member = guild.get_member(p.discord_id)
            DB.create_invitation(p.discord_id, team.name)
            await member.send(
                f"Has sido invitado al grupo {team.name}\nPara formar parte del grupo usa el comando eps!join {team.name}")

    async def join_command(self, ctx):
        from src.modules.facades import ContextFacade
        import src.texts.join_texts as txt
        fac: ContextFacade = ContextFacade(ctx)
        logging.info(f"join command por {fac.get_author().name}")
        user: ModelUser = DB.get_user_from_id(fac.get_author().id)
        if user is None:
            logging.error(f"User {fac.get_author().name} no registrado.")
            ctx.send(txt.USER_NOT_REGISTERED)
            return
        elif user.group_name is not None:
            logging.error(f"User {fac.get_author().name} ya está en un grupo: {user.group_name}")
            ctx.send(txt.USER_ALREADY_IN_TEAM(user.group_name))
        team_name = fac.get_message().split()[1]
        invitation = DB.get_invitation(user.discord_id, team_name)
        if not invitation:
            logging.error(f"User {fac.get_author().name} no tiene invitaciones del grupo {team_name}.")
            ctx.send(txt.NOT_ALLOWED_TEAM(team_name))
            return
        _, invitation = invitation
        if invitation.group_name != team_name:
            logging.error(f"Illegal Statement: {team_name} must be {invitation.group_name}")
            ctx.send(txt.ERROR_SERVER)
            return
        logging.info(f"{fac.get_author().name} invitation del grupo {team_name}")
        DB.accept_invitation(invitation.user_id, invitation.group_name)
        team = DB.get_group(invitation.group_name)
        team.add_user(user.discord_id)
        DB.create_or_update_group(team)
        user.group_name = team_name
        DB.create_or_update_user(user)
        guild = ctx.guild
        role = discord.utils.get(guild.roles, name=team.name)
        member = guild.get_member(user.discord_id)
        logging.info(f"Añadiendo el rol {role.name} al miembro {member.name}")
        await member.add_roles(role)
        await ctx.send(txt.MEMBER_REGISTERED_IN(member.name, role.name))


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
        web_user, group = self.database.recover_web_group_by_user(email)
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
