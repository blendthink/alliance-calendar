FROM python:3.9.4-slim-buster
MAINTAINER info@blendthink.dev

WORKDIR /usr/src/app

RUN apt-get update
RUN apt-get -y install \
    tesseract-ocr \
    tesseract-ocr-jpn \
    libgl1-mesa-dev;
RUN apt-get clean

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
