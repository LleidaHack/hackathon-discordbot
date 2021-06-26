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
REPLY_INDEX_ERR = discord.Embed(
            colour = discord.Colour.red(),
            title = "Error on reply",
            description = " El indice introducido no es correcto o no existe."
)
SEND_TO_ADMINS = lambda id_question, user, question : discord.Embed(
    colour = discord.Colour.blue(),
    title = "#"+id_question + " Question of "+user,
    description = question
)
REPLY_TO_USER = lambda admin, question, reply : discord.Embed(
    colour = discord.Colour.blue(),
    title = "#Tu pregunta ha sido contestada:",
    description = "-"+question+"\n"+"+"+reply+"\n"+"Pregunta contestada por: "+admin
)
NOT_VAlID_CHANNEL = "Este comando no puede ser utilizado en este canal."
EMBED_VOID_MESSAGE = "Tienes que preguntar-me algo, no me llames para luego no decirme nada!! :confused:"