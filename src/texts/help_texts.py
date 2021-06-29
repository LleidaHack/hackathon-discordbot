import discord
from src.texts.const import *

GLOBAL_HELP_MESSAGE = "¡Te he enviado la información por privado! :)"

START_DESCRIPTION_MESSAGE=f"""
¡Ey! Soy **{BOT_NAME}**, *el bot de las tierras de Lleida*. Estoy aquí para ayudarte con los problemas que tengas relacionados con la {EVENT_NAME} {EVENT_YEAR}. :snail:
"""
HELP_COMMAND = "Bueno... creo que este ya sabes lo que hace :grin:"
LOGIN_COMMAND = f"Si te registraste a {EVENT_NAME} {EVENT_YEAR}, ¡ya podrás hacer el **check-in**! :satisfied: Si estás en un equipo, accederás a tus canales privados."
CREATE_COMMAND = "En caso de que inscribieras y no tengas equipo, ¡puedes formar uno! :star_struck: Este comando te permitirá crear un nuevo equipo."
INVITE_COMMAND ="¿Quieres invitar a alguien a tu equipo? :people_with_bunny_ears_partying: "
JOIN_COMMAND = "¿Te han invitado a un equipo? Escribe este comando con el nombre del equipo. :couple:"
LEAVE_COMMAND = "¿Quieres salir del equipo? Con este comando te dejo hacerlo... :smiling_face_with_tear: "
ASK_COMMAND = "Ejecuta este comando si tienes cualquier duda! La haré llegar directamente a los organizadores para que puedan contestarte. :sunglasses:"
JOKE_COMMAND = "¿Un chiste? :woozy_face: "
RPSLS_COMMAND = "Juega conmigo al Rock Paper Scissor Lizard Spock :nerd:"

COMMANDS_DESCRIPTION_MESSAGE=f"""
{START_DESCRIPTION_MESSAGE}
¿En qué te puedo ayudar?
**Aquí tienes mis comandos:**
`{COMMAND_PREFIX}help` {HELP_COMMAND}
`{COMMAND_PREFIX}login` {LOGIN_COMMAND}
`{COMMAND_PREFIX}create <team_name>` {CREATE_COMMAND}
`{COMMAND_PREFIX}invite <discord_user>` {INVITE_COMMAND}
`{COMMAND_PREFIX}join <team_name>` {JOIN_COMMAND}
`{COMMAND_PREFIX}leave` {LEAVE_COMMAND}
`{COMMAND_PREFIX}ask <question>` {ASK_COMMAND}
`{COMMAND_PREFIX}joke` {JOKE_COMMAND}
`{COMMAND_PREFIX}rpsls <option>` {RPSLS_COMMAND}
"""

EMBED_HELP_MESSAGE = discord.Embed(
    colour=discord.Colour.blue(),
    title=f"{EVENT_NAME} {EVENT_YEAR}",
    description=COMMANDS_DESCRIPTION_MESSAGE
)
SERVER_ERROR="¡Vaya! Hemos tenido un problemilla con el servidor, ya está informado :grin:"
INVALID_COMMAND=f"¿Has escrito bien el comando? Escribe `{COMMAND_PREFIX}help` si quieres saber los comandos :satisfied:"


QUIM_TEXT=f"""
{BOT_NAME} commands

{COMMAND_PREFIX}help: Si necesitas ayuda par ver mejor como funciona Lo Bot, usa este comando.

{COMMAND_PREFIX}login: Si previamente te registraste a {EVENT_NAME} {EVENT_YEAR} mediante la web, deberás ejecutar este comando para registrarte. Una vez registrado si eres el primero de tu equipo se creará un canal de voz i de texto privado para ti.

{COMMAND_PREFIX}create <team_name>: En caso de que inscribieras y no tengas equipo puedes formar uno! Este comando te permitirá crear un nuevo equipo.

{COMMAND_PREFIX}join <team_name>: Si no tenías equipo y alguien te ha autorizado a que entres al suyo debes ejecutar este comando para unirte al equipo.

{COMMAND_PREFIX}invite <discord_user>: Si quieres invitar a alguien a tu equipo usa este comando.

{COMMAND_PREFIX}leave <team_name>: En caso de que quieras salir de un grupo este es el comando que debes usar.

{COMMAND_PREFIX}ask <question>: Ejecuta este comando si tienes cualquier duda! Lo Bot nos la hará llegar directamente a los organizadores para que podamos contestar-la!

{COMMAND_PREFIX}joke: Si ejecutas este comando Lo Bot te contará un chiste. (No nos hacemos responsables de lo malos que puedan ser)

{COMMAND_PREFIX}rpsls <option>: Juega al Rock Paper Scissor Lizard Spock con nuestro bot."""
