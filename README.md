# HackEPS 2020 - Discord

## Usage

**Package Requirements**:
 > `python3`\
 > `python3-pip`
 
**Pip modules requirements**:
 >`firebase_admin`\
 > `python-dotenv`\
 > `discord`

**Installation**
> **1. Clone repository**
```
git clone https://github.com/LleidaHack/hackeps-2020-discordbot
```

> **2. Install requierements**
Ensure that you have python3 and python3-pip installed.
```
python3 --version
pip3 --version
```
if you don't, you can install it from the official sources:\
**Python3: `https://www.python.org/download/releases/3.0/`**\
**PIP3: `https://www.pypa.io/en/latest/`**

The following step is install the required packages using pip
```
python3 -m pip install -r requirements.txt
```

> **3. Configure .env**

First of all, we have to copy `.env.sample` file to `.env`.\
**Linux and Windows PowerShell**
```
$ cp .env.sample .env
```
**Windows CMD**
```
> copy .env.sample .env
```

After that, we have to fill the **`.env`** (notice that **YOU DON'T HAVE TO TOUCH** `.env.sample`) with your bot information:
```
# ------------------------------------------------------------------------------#
#---------------------------HACKEPS 2020 DISCORD BOT----------------------------#
# ------------------------------------------------------------------------------#



#-----------------------------Discord Configuration-----------------------------#
DISCORD_TOKEN={Discord bot token}
DISCORD_PREFIX={Bot command prefix}
GUILD={Guild of the bot ID}
TEAMS_CATEGORY_ID ={The category ID from the guild where the teams channels will be created}
LOG_ERROR_CHANNEL_ID={The channel ID where the bot will throw a stack excepcion if something wrong happens}
INFO_BOT_CHANNEL_ID={The channel where the bot will write the bot information}
HACKER_ROLE={Name of the rol for the logged users}
#-----------------------------Database Configuration----------------------------#
#----------------------------------HackEPS 2020---------------------------------#
HACKESP2020_DB_PATH={The insciption webpage database path on firebase}
DISCORD_DB_PATH={The bot database path on firebase}
```

> **4. Execution**

In order to execute it, you have to run the bot.py python file. A way to do it is using the following command:
```
python3 bot.py
```
## How to adapt to my own bot

## Unit Test
```
python -m unittest
```
