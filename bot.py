#!/usr/bin/python3
import sys, os
        
import logging
from dotenv import load_dotenv
if len(sys.argv) != 1:
    load_dotenv(sys.argv[1])
else:
    load_dotenv()
    logging.basicConfig(level=logging.DEBUG)
logging.debug("Reading env configuration")
from src.modules.discord_bot import DiscordBot

if __name__ == "__main__":

    bot = DiscordBot()
    bot.start()

