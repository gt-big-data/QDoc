#!/bin/sh -eu

cd /home/bdc/QDoc/
echo $(date) >> QDocRuns.log
QDOC_ENV=prod python crawler.py
