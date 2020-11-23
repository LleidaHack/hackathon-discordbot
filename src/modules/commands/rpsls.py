import logging
import random

from discord.ext.commands import Context

from src.modules.commands import BaseCommand


class GameCommand(BaseCommand):

    def __init__(self, context: Context):
        super().__init__(context)
        self.options = ['rock', 'paper', 'scissors', 'lizard', 'spock']
        self.win_conditions = [('paper', 'disaproves', 'spock'),
                               ('paper', 'covers', 'rock'),
                               ('rock', 'crushes', 'scissors'),
                               ('rock', 'crushes', 'lizard'),
                               ('lizard', 'eats', 'paper'),
                               ('lizard', 'poisons', 'spock'),
                               ('spock', 'vaporizes', 'rock'),
                               ('spock', 'smashes', 'scissors'),
                               ('scissors', 'cuts', 'paper'),
                               ('scissors', 'decapicates', 'lizard')
                               ]

    async def apply(self):
        first_to_uppercase = lambda word : word[0].upper()+word[1:]
        logging.info(f"apply de JokeCommand")
        msg = self.ctx.message.content.split()
        if len(msg) == 1:
            await self.ctx.channel.send("Tienes que poner una de estas opciones: Rock, Paper, Scissor, Lizard, Spock.")
        player_choice = msg[1].lower()
        if player_choice in self.options:
            bot_choice = random.choice(self.options)
            if player_choice == bot_choice:
                await self.ctx.channel.send(
                    'Ni pa ti ni pa mi, empate.:exploding_head: ' + first_to_uppercase(player_choice) + ' shake hands ' + first_to_uppercase(bot_choice))
            for i in self.win_conditions:
                if bot_choice == i[0] and player_choice == i[2]:
                    await self.ctx.channel.send(
                        'Lo siento pero... He ganado:sunglasses: ' + first_to_uppercase(i[0]) + ' ' + i[1] + ' ' + first_to_uppercase(i[2]))
                if player_choice == i[0] and bot_choice == i[2]:
                    await self.ctx.channel.send('Tu ganas :tired_face: ' + first_to_uppercase(i[0]) + ' ' + i[1] + ' ' + first_to_uppercase(i[2]))
        else:
            await self.ctx.channel.send("Tienes que poner una de estas opciones: Rock, Paper, Scissor, Lizard, Spock.")
