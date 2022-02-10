# pull image
FROM postgres:latest

# bash aliases
COPY ./docker/.bashrc /root/.bashrc

# init script
COPY ./docker/dev/postgres/init-db.sh /docker-entrypoint-initdb.d/01-db-setup.sh
RUN chmod +x /docker-entrypoint-initdb.d/01-db-setup.sh