# syntax=docker/dockerfile:1.7
FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

RUN useradd --create-home django && chown -R django /app
USER django

ENV DJANGO_SETTINGS_MODULE=ecopoweratlas.settings
EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "ecopoweratlas.wsgi:application"]
