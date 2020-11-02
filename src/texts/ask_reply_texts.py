import discord

GLOBAL_ASK_MESSAGE = "¡Te he enviado la información por privado! :)"
EMBED_ASK_MESSAGE = discord.Embed(
            colour = discord.Colour.blue(),
            title="HackEPS 2020",
            description=
            """
                ¡Ey! tu pregunta ha sido enviada a la organizacion, en cuanto puedan te van a responder.
            """
        )
EMBED_REPLY_MESSAGE = discord.Embed(
            colour = discord.Colour.green(),
            title = "Tu respuesta ya ha llegado"
)
REPLY_INDEX_ERR =discord.Embed(
            colour=discord.Colour.red(),
            title="Error on reply",
            description=" El indice introducido no es correcto o no existe."
)
NOT_VAlID_CHANNEL="Este comando no puede ser utilizado en este canal."