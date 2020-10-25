FROM python:alpine3.12

WORKDIR /lleidahack/bot

COPY requirements.txt .


RUN pip install --upgrade pip 

RUN pip install -r requirements.txt

COPY src/ .

ENV DISCORD_TOKEN discord_token

ENV HACKESP2020_DB_PATH db_hack

ENV DISCORD_DB_PATH db_discord

RUN chmod +x script.sh 

ENTRYPOINT ["./script.sh", "${DISCORD_TOKEN}", "${HACKESP2020_DB_PATH}","${DISCORD_DB_PATH}"]
