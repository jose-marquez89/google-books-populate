FROM ubuntu:18.04

### For reliable logging/io
ENV PYTHONBUFFERED=1

### libpq-dev is for building psycopg2
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y python3-pip python3-dev libpq-dev cron

ENV SHELL=/bin/bash

RUN mkdir /app

### Copy requirements first to leverage cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

EXPOSE 80

RUN chmod +x run-populate
ADD rootCrontab /etc/cron.d/populate-cron

RUN chmod 0644 /etc/cron.d/populate-cron

CMD cron && tail -f /app/background.log
