#!/bin/sh

while true; do
  nohup python download.py >> test.out
  sleep 5
done &
