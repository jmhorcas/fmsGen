FROM nginx:1.25-alpine

LABEL name="fmsGenNginx"

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d