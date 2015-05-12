#!/bin/bash 
cd /home/QDoc/
echo $(date) >> QDocRuns.log
python crawler.py
