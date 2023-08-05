#!/bin/bash
python DatabaseCreate.py
uwsgi \
  --http-socket 0.0.0.0:8051 \
  --master \
  --die-on-term \
  -p 1 \
  --wsgi-file /usr/src/app/UniqueIDServer.py "$@"
