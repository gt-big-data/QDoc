#!/bin/sh -eu

cd /home/QDoc/
# TODO: Move this date stamp to Python.
echo $(date) >> QDocRuns.log
python crawler.py
