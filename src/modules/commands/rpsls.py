import logging
import random

from discord.ext.commands import Context

from src.modules.commands import BaseCommand


class GameCommand(BaseCommand):

    def __init__(self, context: Context):
        super().__init__(context)
        self.options = ['Rock', 'Paper', 'Scissors', 'Lizard', 'Spock']
        self.win_conditions = [('Paper', 'disaproves', 'Spock'),
                               ('Paper', 'covers', 'Rock'),
                               ('Rock', 'crushes', 'Scissors'),
                               ('Rock', 'crushes', 'Lizard'),
                               ('Lizard', 'eats', 'Paper'),
                               ('Lizard', 'poisons', 'Spock'),
                               ('Spock', 'vaporizes', 'Rock'),
                               ('Spock', 'smashes', 'Scissors'),
                               ('Scissors', 'cuts', 'Paper'),
                               ('Scissors', 'decapicates', 'Lizard')
                               ]

    async def apply(self):
        logging.info(f"apply de JokeCommand")
        msg = self.ctx.message.content.split()
        if len(msg) == 1:
            await self.ctx.channel.send("Tienes que poner una de estas opciones: Rock, Paper, Scissor, Lizard, Spock.")
        player_choice = msg[1]
        if player_choice in self.options:
            bot_choice = random.choice(self.options)
            if player_choice == bot_choice:
                await self.ctx.channel.send(
                    'Ni pa ti ni pa mi, empate.:exploding_head: ' + player_choice + ' shake hands ' + bot_choice)
            for i in self.win_conditions:
                if bot_choice == i[0] and player_choice == i[2]:
                    await self.ctx.channel.send(
                        'Lo siento pero... He ganado:sunglasses: ' + i[0] + ' ' + i[1] + ' ' + i[2])
                if player_choice == i[0] and bot_choice == i[2]:
                    await self.ctx.channel.send('Tu ganas :tired_face: ' + i[0] + ' ' + i[1] + ' ' + i[2])
        else:
            await self.ctx.channel.send("Tienes que poner una de estas opciones: Rock, Paper, Scissor, Lizard, Spock.")
