FROM python:3.9.1-slim-buster

WORKDIR /web

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
  pip install --upgrade pip && \
  apt install --no-install-recommends gcc -y && \
  rm -rf /var/lib/apt/lists/*
COPY ./* /web/
RUN pip install -r requirements.txt
CMD python manage.py runserver 0.0.0.0:$PORT
