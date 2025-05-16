# Dockerfile for the python based API for neptune
FROM python:3.13-bullseye

WORKDIR /api

RUN apt-get update

COPY ./Pipfile Pipfile

COPY ./Pipfile.lock Pipfile.lock

RUN pip install pipenv && pipenv install

COPY . .

CMD pipenv run gunicorn -b 0.0.0.0:8000 -k 4 -k uvicorn.workers.UvicornWorker app.main:app
