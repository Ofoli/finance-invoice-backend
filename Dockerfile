FROM python:3.11-alpine

COPY ./requirements.txt ./requirements.txt
COPY ./app ./app

RUN apk add --no-cache postgresql-libs && \
    apk add --no-cache postgresql-dev && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r ./requirements.txt 
    
WORKDIR /app

EXPOSE 8800