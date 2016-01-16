#!/bin/sh -eu

cd /home/bdc/QDoc/
echo $(date) >> QDocRuns.log
python crawler.py
