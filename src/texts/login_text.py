import discord
from src.texts.const import *

WELCOME_MESSAGE = discord.Embed(
    colour=discord.Colour.blue(),
    title=f"¡Bienvenido a la {EVENT_NAME} {EVENT_YEAR}",
    description=
    f"""
        ¡Hola!
        Permiteme que sea el primero en darte la bienvenida a esta 4a edición de la {EVENT_NAME} en nombre de toda la organización.
        Mi nombre es LoBot :snail: y estoy aquí para ayudar a los LleidaHackers con la organización. Puedes usar el comando `{COMMAND_PREFIX}help` para ver la ayuda.```
    """
)
REGISTER_STARTING = "Aha... Vale, dame unos segundos que tengo que revisar la base de datos :eyes:" 
REGISTER_MESSAGE = f"Primero de todo necesito verificar que estás inscrito en la {EVENT_NAME}... ¿Con qué correo te inscribiste? "
REGISTER_OK = "¡Perfecto! Te has conectado correctamente. :smiley_cat: "
REGISTER_YOU_ARE_LOGGED = "¡Pero si ya estás conectado! Si tienes algún problema contacta con un organizador."
REGISTER_ALREADY_REGISTER = f"Parece que este usuario ya está conectado :worried:. Ponte en contacto con un administrador si se trata de un error o escribe `{COMMAND_PREFIX}login` para volver a intentarlo."
REGISTER_KO = f"Uy... Me temo que no encuentro este correo en la base de datos. Utiliza `{COMMAND_PREFIX}login` para volver a empezar o ponte en contacto con un LleidaHacker de carne y hueso mediante MP"
PM_SENDED= "Esto mejor lo comentamos por privado..."
def USER_HAS_GROUP(group):
    return f"¡Todo correcto! Dame un segundo que te añado al grupo {group} :wink:"

def USER_NO_GROUP(name, discriminator):
    return f"¡Te encontré! Pero parece que no apuntaste ningún grupo. Puedes usar los canales de reclutamiento para buscar equipo. Con el comando `{COMMAND_PREFIX}create` puedes crear un equipo o pídele a tus compañeros que te inviten mediante `eps!invite {name}#{discriminator}`"