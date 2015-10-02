#!/usr/bin/env python
"""Check how many articles were added in the last N hours."""

from dbco import *
import time

while(True):
    ts = time.time();
    ts = ts - int(raw_input('Number of articles in the last X hours?'))*60*60;
    nb = db.qdoc.find({'timestamp': {'$gte': ts}}).count()
    print nb, ' articles';
