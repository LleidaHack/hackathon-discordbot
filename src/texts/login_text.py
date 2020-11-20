import discord

WELCOME_MESSAGE = discord.Embed(
    colour=discord.Colour.blue(),
    title="¡Bienvenido a la HackEPS2020",
    description=
    """
        ¡Hola!
        Permiteme que sea el primero en darte la bienvenida a esta 4a edición de la HackEPS en nombre de toda la organización.
        Mi nombre es LoBot y estoy aquí para ayudar a los LleidaHackers con la organización. Puedes usar el comando eps!help para ver la ayuda.```
    """
)
REGISTER_MESSAGE = "Vamos a ver que reviso la lista... ¿Cuál es tu usuario con el que te has inscrito a la HackEPS?"
REGISTER_OK = "¡Perfecto! Te has conectado correctamente."
REGISTER_ALREADY_REGISTER = "Parece que ya estás registrado. Ponte en contacto con un administrador si se trata de un error."
REGISTER_KO = "Uy... Me temo que no te encuentro en la base de datos. Utiliza eps!register para volver a empezar el registro o ponte en contacto con un LleidaHacker de carne y hueso mediante MP"
USER_HAS_GROUP = "Te he añadido a grupo"
USER_NO_GROUP = "Parece que no tienes grupo. Puedes usar los canales de reclutamiento y el comando eps!create o eps!join para crear o unirte a un grupo"
PM_SENDED= "Esto mejor lo comentamos por privado..."