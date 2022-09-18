FROM --platform=arm64 python:alpine

RUN apk add --no-cache bash 

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt