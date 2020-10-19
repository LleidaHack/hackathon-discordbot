FROM python:3.8

WORKDIR /lleidahack/bot

COPY requirements.txt .

RUN pip install -r requierements.txt

COPY src/ .

CMD [ "python", "./server.py" ]