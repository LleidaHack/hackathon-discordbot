#!/usr/bin/python3
from dotenv import load_dotenv
from src.modules.discord_bot import DiscordBot
import logging
import random
import discord

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("Reading env configuration")
    load_dotenv()
    bot = DiscordBot()
    client = discord.Client()
    bot.start()


    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        chistes = [
            "- ¿Por que los de Lepe ponen internet en la ventana?\n- Para tener windows vista.",
            "- ¿Cuántos técnicos de Microsoft hacen falta para cambiar una bombilla?\n- Ninguno, es un problema de Hardware.",
            "- ¿Qué es el hardware?\n- El que recibe los golpes cuando falla el software.",
            "- ¿Cuál es el plato preferido de los informáticos?\n- Las patatas chips.",
            "- ¿AlguienSabeComoArreglarLaBarraEspaciadora?",
            "- ¿Cuál es el virus más extendido del mundo?\n- El Sistema Windows.",
            "- Abuelo, por qué estás delante del ordenador con los ojos cerrados?\n- Esque me ha pedido que cierre las pestañas.",
            "- Venga, bueno, aceptamos Windows Vista como Sistema Operativo.",
            "- ¿Cuál es la canción favorita de un caracol?\n- Despacito.",
            "- ¿Por qué McDonald's no sirve caracoles?\n- Porque no son comida rápida.",
            "- Va un caracol y derrapa."]

        if message.content == 'joke':
            response = random.choice(chistes)
            await message.channel.send(response)
