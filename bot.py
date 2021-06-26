#!/usr/bin/python3
import sys

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

    bot = DiscordBot()
    bot.start()

