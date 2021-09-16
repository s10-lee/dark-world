FROM nginx:latest

COPY ./docker/.bashrc /root/.bashrc

# RUN rm /etc/nginx/conf.d/default.conf

# Basic Auth
# COPY ./docker/prod/nginx/.htpasswd /etc/nginx/.htpasswd

# Payer Confirm
# COPY ./docker/prod/nginx/payeer_1120238364.txt  /usr/src/app/files/payeer_1120238364.txt

COPY ./docker/dev/nginx/default.conf /etc/nginx/conf.d/default.conf

COPY ./docker/dev/nginx/dhparam-2048.pem /etc/ssl/certs/dhparam-2048.pem

COPY ./docker/dev/nginx/localhost.crt /etc/letsencrypt/common/localhost.crt
COPY ./docker/dev/nginx/localhost.key /etc/letsencrypt/common/localhost.key

#openssl req -x509 -nodes -newkey rsa:2048 -days 1 \
#-keyout /etc/letsencrypt/live/labgrow.io/privkey.pem \
#-out "$path/fullchain.pem" \
#-subj '/CN=localhost'"
