FROM python:3.11-bullseye

WORKDIR /django_rest/app

COPY . /django_rest/app

EXPOSE 8000

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
