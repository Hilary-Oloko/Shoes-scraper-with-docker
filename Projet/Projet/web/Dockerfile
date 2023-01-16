# utiliser une image Python en tant que base
FROM python:3.8

RUN apt-get update && apt-get upgrade -y

RUN pip install --upgrade pip

WORKDIR /app

ADD . .

RUN pip install -r requirements.txt

CMD python ./app.py