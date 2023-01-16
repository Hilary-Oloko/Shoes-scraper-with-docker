FROM python

RUN apt-get update && apt-get upgrade -y

RUN pip install --upgrade pip

RUN pip install scrapy

RUN pip install pymongo requests

RUN mkdir -p /scrapy

WORKDIR /scrapy