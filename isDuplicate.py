from difflib import SequenceMatcher
import sys, random, time
from article import *
from dbco import *

def similar(a, b):
	rat = len(a)/float(len(b))
	if rat < 0.9 or rat > 1.1:
		return 0
	return SequenceMatcher(None, a, b).ratio()

def isDuplicate(content, title, source):
	last = db.qdoc.find({'source': source, 'timestamp': {'$gte': (time.time()-3*86400)}}) # last 3 days
	for a in last:
		if title == a['title'] or similar(content, a['content']) > 0.9:
			return a['_id']
	return None