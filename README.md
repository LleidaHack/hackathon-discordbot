# Hackathon Bot - Discord
**NOTE** DEPRECATED BOT. STAND BY FOR A NEW VERSION
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
git clone https://github.com/LleidaHack/hackathon-discordbot
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
#-------------------------HACKATHON DISCORD BOT--------------------------#
# ------------------------------------------------------------------------------#



#-----------------------------Discord Configuration-----------------------------#
DISCORD_TOKEN=
DISCORD_PREFIX=
GUILD=
LOG_ERROR_CHANNEL_ID=
INFO_BOT_CHANNEL_ID=
HACKER_ROLE=Hacker
ADMIN_ROLE=LleidaHacker
GOOGLE_CREDENTIALS=

GOOGLE_APPLICATION_CREDENTIALS=src/certificate.json
#-----------------------------Database Configuration----------------------------#
# hackeps = se lee la base de datos de participantes de hackeps
# csv = Lectura de CSV con los emails de los participantes
USER_AUTHTYPE=csv
HACKEPS_DB_PATH=
CSV_PATH =

#----------------------------------BOT DATABASE---------------------------------#
DISCORD_DB_PATH=



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
