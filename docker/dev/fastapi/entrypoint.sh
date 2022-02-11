#!/bin/bash


/wait-for-it.sh db:5432 -t 10 && /usr/local/bin/gunicorn \
  -b 0.0.0.0:8000 \
  -w 4 \
  -k uvicorn.workers.UvicornWorker app.main:app \
  --chdir . \
  --log-level debug \
  --disable-redirect-access-to-syslog
