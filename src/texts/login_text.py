import discord


def send_message_login(name):
    return f"{name} Te he enviado la información por privado para registrarte."


EMBED_LOGIN_MESSAGE = discord.Embed(
    colour=discord.Colour.blue(),
    title="HackEPS 2020 login",
    description=
    """
        ¡Ey! Soy Lo Bot, el bot de las tierras de Lleida. Me han programado para ayudarte con los problemas que tengas relacionados con la HackEPS 2020. ¿En qué te puedo ayudar?
        Comandos disponibles:
        ```eps!help -> Bueno... creo que este ya sabes lo que hace ;)```
    """
)
