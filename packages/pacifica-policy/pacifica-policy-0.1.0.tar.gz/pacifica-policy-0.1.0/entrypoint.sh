#!/bin/bash
uwsgi \
  --http-socket 0.0.0.0:8181 \
  --master \
  --die-on-term \
  --wsgi-file /usr/src/app/pacifica/policy/wsgi.py "$@"
