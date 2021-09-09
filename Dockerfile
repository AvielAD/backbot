FROM python:3.8-slim-buster

RUN apt update
RUN apt install build-essential -y

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8080

CMD [ "python3", "servercopy.py" ]
