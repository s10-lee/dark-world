# pull image
FROM postgres:13

# bash aliases
COPY ./docker/.bashrc /root/.bashrc

# init script
COPY ./docker/prod/postgres/init-db.sh /docker-entrypoint-initdb.d/01-db-setup.sh
RUN chmod +x /docker-entrypoint-initdb.d/01-db-setup.sh