FROM python:3.11-alpine

ENV TZ UTC

COPY ./requirements.txt ./requirements.txt
COPY ./app ./app

RUN apk add --no-cache postgresql-libs && \
    apk add --no-cache postgresql-dev && \
    apk add --no-cache gcc musl-dev python3-dev && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r ./requirements.txt 
    
WORKDIR /app

EXPOSE 8800