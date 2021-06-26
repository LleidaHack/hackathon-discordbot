#!/usr/bin/python3
import sys, os

from dotenv import load_dotenv
if len(sys.argv) != 1:
    load_dotenv(sys.argv[1])
else:
    load_dotenv()
from src.modules.discord_bot import DiscordBot
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("Reading env configuration")

    if not os.path.isfile(os.getenv('GOOGLE_APPLICATION_CREDENTIALS')):
        with open(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'), 'w') as file:
            file.write(os.getenv('GOOGLE_CREDENTIALS'))
    bot = DiscordBot()
    bot.start()

