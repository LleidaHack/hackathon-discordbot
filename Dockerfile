FROM python:3.9.6-alpine3.14



WORKDIR /hackathon-bot

COPY requirements.txt .



RUN python3 -m pip install --upgrade pip 

RUN python3 -m pip install -r requirements.txt

COPY src/ .

CMD ["python3", "bot.py"]