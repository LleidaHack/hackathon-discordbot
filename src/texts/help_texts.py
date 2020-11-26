import discord

GLOBAL_HELP_MESSAGE = "¡Te he enviado la información por privado! :)"

START_DESCRIPTION_MESSAGE="""
¡Ey! Soy **Lo Bot**, *el bot de las tierras de Lleida*. Estoy aquí para ayudarte con los problemas que tengas relacionados con la HackEPS 2020. :snail:
"""
HELP_COMMAND = "Bueno... creo que este ya sabes lo que hace :grin:"
LOGIN_COMMAND = "Si te registraste a HackEPS2020, ¡ya podrás hacer el **check-in**! :satisfied: Si estás en un equipo, accederás a tus canales privados."
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
`eps!help` {HELP_COMMAND}
`eps!login` {LOGIN_COMMAND}
`eps!create <team_name>` {CREATE_COMMAND}
`eps!invite <discord_user>` {INVITE_COMMAND}
`eps!join <team_name>` {JOIN_COMMAND}
`eps!leave` {LEAVE_COMMAND}
`eps!ask <question>` {ASK_COMMAND}
`eps!joke` {JOKE_COMMAND}
`eps!rpsls <option>` {RPSLS_COMMAND}
"""

EMBED_HELP_MESSAGE = discord.Embed(
    colour=discord.Colour.blue(),
    title="HackEPS 2020",
    description=COMMANDS_DESCRIPTION_MESSAGE
)

QUIM_TEXT="""
Lo Bot commands

eps!help: Si necesitas ayuda par ver mejor como funciona Lo Bot, usa este comando.

eps!login: Si previamente te registraste a HackEPS2020 mediante la web, deberás ejecutar este comando para registrarte Hacker. Una vez registrado si eres el primero de tu equipo se creará un canal de voz i de texto privado para ti.

eps!create <team_name>: En caso de que inscribieras y no tengas equipo puedes formar uno! Este comando te permitirá crear un nuevo equipo.

eps!join <team_name>: Si no tenías equipo y alguien te ha autorizado a que entres al suyo debes ejecutar este comando para unirte al equipo.

eps!invite <discord_user>: Si quieres invitar a alguien a tu equipo usa este comando.

eps!leave <team_name>: En caso de que quieras salir de un grupo este es el comando que debes usar.
eps!ask <question>: Ejecuta este comando si tienes cualquier duda! Lo Bot nos la hará llegar directamente a los organizadores para que podamos contestar-la!

eps!joke: Si ejecutas este comando Lo Bot te contará un chiste. (No nos hacemos responsables de lo malos que puedan ser)

eps!rpsls <option>: Juega al Rock Paper Scissor Lizard Spock con nuestro bot."""
