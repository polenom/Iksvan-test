FROM python:3.10
RUN apt-get update -y && apt-get upgrade -y

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install -r requirements.txt
COPY ./ ./
#RUN python3 manage.py makemigrations && python3 manage.py migrate
