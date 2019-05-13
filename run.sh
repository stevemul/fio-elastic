#!/bin/bash

sh /opt/check.sh

for i in $JOBFILES; do fio --output-format json --output=fio-output.json $i; \
  /usr/bin/python /opt/elastic-push.py -f /tmp/fio-data/fio-output.json -s $ES_SERVER; \
  done
