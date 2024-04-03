FROM python:3.10-alpine

WORKDIR /8inf349

COPY . .

RUN apk update
RUN apk add gcc musl-dev postgresql-dev

RUN pip install -r requirements.txt

ENV FLASK_APP=api8inf349

CMD flask init-db; flask worker & flask run --host=0.0.0.0
