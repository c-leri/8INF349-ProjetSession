# syntax=docker/dockerfile:1.7-labs
FROM python:3.10-alpine

WORKDIR /8inf349

COPY --exclude=./ui/ . .

RUN apk update
RUN apk add gcc musl-dev postgresql-dev

RUN pip install -r requirements.txt
RUN pip install gunicorn

ENV FLASK_APP=api8inf349

CMD flask init-db; flask worker & gunicorn "$FLASK_APP:create_app()" -b 0.0.0.0:5000 -w 4
