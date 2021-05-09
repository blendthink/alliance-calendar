FROM python:3.9.4-slim-buster
MAINTAINER info@blendthink.dev

# update and install depedencies
RUN apt-get update -y && \
    apt-get install -y wget unzip bc vim libleptonica-dev git

# install packages to complie Tesseract
RUN apt-get install -y --reinstall make && \
    apt-get install -y g++ autoconf automake libtool pkg-config \
     libpng-dev libjpeg62-turbo-dev libtiff5-dev libicu-dev \
     libpango1.0-dev autoconf-archive

# install & unzip
RUN wget https://github.com/tesseract-ocr/tesseract/archive/5.0.0-alpha-20210401.zip && \
	unzip 5.0.0-alpha-20210401.zip

# compile
RUN cd tesseract-5.0.0-alpha-20210401 && \
    ./autogen.sh && \
    ./configure && \
    make && make install && ldconfig && \
    make training && make training-install

# download best trained data
RUN cd /usr/local/share/tessdata && \
    wget https://github.com/tesseract-ocr/tessdata_best/raw/master/eng.traineddata && \
    wget https://github.com/tesseract-ocr/tessdata_best/raw/master/jpn.traineddata

# setting the data prefix
ENV TESSDATA_PREFIX=/usr/local/share/tessdata

# setup openCV
RUN apt-get install -y libgl1-mesa-dev

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
