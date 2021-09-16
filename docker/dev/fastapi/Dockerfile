# pull the official docker image
FROM python:3.9-slim

# command aliases
COPY ./docker/dev/fastapi/.bashrc /root/.bashrc

# wait for database script
COPY ./docker/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# set work directory
WORKDIR /app

# copy project
COPY ./app .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# init and migrate db
# TODO: not working !
# RUN python ./air init -t src.settings.ORM --location ./db/migrations
# RUN python ./air init-db

# Env
ENV ACCESS_LOG=${ACCESS_LOG:-/proc/1/fd/1}
ENV ERROR_LOG=${ERROR_LOG:-/proc/1/fd/2}

ENTRYPOINT /wait-for-it.sh db:5432 -t 10 && /usr/local/bin/gunicorn \
  -b 0.0.0.0:8000 \
  -w 4 \
  -k uvicorn.workers.UvicornWorker src.main:app \
  --chdir /app \
  --log-level debug \
  --access-logfile "$ACCESS_LOG" \
  --error-logfile "$ERROR_LOG" \
  --disable-redirect-access-to-syslog
