# syntax=docker/dockerfile:1
FROM python:3.8.10-slim-buster

WORKDIR /xesque-bot

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]