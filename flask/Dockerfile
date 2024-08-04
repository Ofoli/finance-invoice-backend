FROM python:3.11-alpine

COPY ./requirements.txt ./requirements.txt
COPY ./app ./app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r ./requirements.txt

WORKDIR /app

EXPOSE 8800