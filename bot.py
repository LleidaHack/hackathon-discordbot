#!/usr/bin/python3
from dotenv import load_dotenv
from src.modules.discord_bot import DiscordBot
import logging
import sys

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("Reading env configuration")
    if len(sys.argv) != 1:
        load_dotenv(sys.argv[1])
    else:
        load_dotenv()
    bot = DiscordBot()
    bot.start()

