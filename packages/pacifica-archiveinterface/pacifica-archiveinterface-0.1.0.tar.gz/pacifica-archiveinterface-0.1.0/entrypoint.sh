#!/bin/bash

uwsgi \
  --http-socket $PACIFICA_AAPI_ADDRESS:$PACIFICA_AAPI_PORT \
  --master \
  --die-on-term \
  --wsgi-file /usr/src/app/archiveinterface/wsgi.py "$@"
