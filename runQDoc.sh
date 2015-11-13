#!/bin/sh -eu

cd /home/QDoc/
echo $(date) >> QDocRuns.log
python crawler.py
