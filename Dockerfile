FROM python:3.8-slim-buster

MAINTAINER Harry Wright "harry@wright.dev"

RUN apt update
RUN apt install -y libpq-dev python3-dev build-essential

EXPOSE 5000

RUN mkdir /app
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

CMD ["python3", "app.py"]