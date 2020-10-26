#!/usr/bin/python3
from dotenv import load_dotenv
from modules.discord_bot import DiscordBot
import logging
<<<<<<< HEAD
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("Reading env configuration")
    load_dotenv()

=======

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("Reading env configuration")
    load_dotenv()

>>>>>>> 3fd4d3cdfcadd1e14b426ea7cc3732d18fb68331
    bot = DiscordBot()
    bot.start()
