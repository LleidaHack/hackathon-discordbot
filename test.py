#!/usr/bin/python3
from dotenv import load_dotenv
from testbot.bot import TestBot
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("Reading env configuration")
    load_dotenv('.envtest')
    bot = TestBot()
    bot.start()