#!/bin/bash
# -*- ENCODING: UTF-8 -*-
echo DISCORD_TOKEN=$1 > .env 
echo HACKESP2020_DB_PATH=$2 >> .env
echo DISCORD_DB_PATH=$3 >> .env

python3 ./bot.py


