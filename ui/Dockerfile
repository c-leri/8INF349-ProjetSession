# syntax=docker/dockerfile:1.7-labs
FROM nginx:1.25.4

COPY ./nginx-configs /etc/nginx/conf.d

COPY --exclude=./nginx-configs/ . /usr/share/nginx/ui
