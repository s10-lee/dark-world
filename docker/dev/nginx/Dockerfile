FROM nginx:latest

COPY ./docker/.bashrc /root/.bashrc

# Basic Auth
# COPY ./docker/prod/nginx/.htpasswd /etc/nginx/.htpasswd

COPY ./docker/dev/nginx/default.conf /etc/nginx/conf.d/default.conf
COPY ./docker/dev/nginx/dhparam-2048.pem /etc/ssl/certs/dhparam-2048.pem

COPY ./docker/dev/nginx/localhost.crt /etc/letsencrypt/common/localhost.crt
COPY ./docker/dev/nginx/localhost.key /etc/letsencrypt/common/localhost.key

#openssl req -x509 -nodes -newkey rsa:2048 -days 1 \
#-keyout /etc/letsencrypt/live/labgrow.io/privkey.pem \
#-out "$path/fullchain.pem" \
#-subj '/CN=localhost'"
