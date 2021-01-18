FROM ubuntu:20.04

WORKDIR /app
RUN mkdir static/ && mkdir media/

RUN apt update && \
  apt install -y python3-pip python3-dev

COPY ./products products/
COPY ./Shop Shop/
COPY ./templates templates/
COPY ./manage.py .
COPY ./requirements.txt .
COPY ./data.json .

RUN pip3 install -r requirements.txt && \
  python3 manage.py migrate && \
  python3 manage.py loaddata data.json
