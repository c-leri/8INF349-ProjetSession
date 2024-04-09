# syntax=docker/dockerfile:1.7-labs
FROM nginx

COPY ./nginx-configs /etc/nginx/conf.d

COPY --exclude=./nginx-configs/ . /usr/share/nginx/ui
