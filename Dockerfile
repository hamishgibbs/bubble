FROM python:3

RUN apt-get update && apt-get install make

COPY requirements.txt ./
RUN pip install -U pip && pip install --no-cache-dir -r requirements.txt

WORKDIR /usr/bubble

COPY . .
