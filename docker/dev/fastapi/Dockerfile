# pull the official docker image
FROM python:3.9-slim

# command aliases
COPY ./docker/.bashrc /root/.bashrc

COPY ./docker/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

COPY ./docker/dev/fastapi/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./requirements.txt .

RUN pip install -U pip
RUN pip install --no-cache-dir -r requirements.txt


WORKDIR /usr/src

COPY ./app ./app
COPY ./stats ./stats

COPY ./app/cli/cmd.py ./cli
RUN chmod +x ./cli

RUN alias cli="/usr/src/app/cli"

ENTRYPOINT ["/entrypoint.sh"]

#ENTRYPOINT /wait-for-it.sh db:5432 -t 10 && /usr/local/bin/gunicorn \
#  -b 0.0.0.0:8000 \
#  -w 4 \
#  -k uvicorn.workers.UvicornWorker app.main:app \
#  --chdir . \
#  --log-level debug \
#  # --access-logfile "$ACCESS_LOG" \
#  # --error-logfile "$ERROR_LOG" \
#  --disable-redirect-access-to-syslog
