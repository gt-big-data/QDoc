from collections import Counter
from dbco import *

articles = db.qdoc.find()

titles = []
sources = {}

for article in articles:
	t = article['title']
	titles.append(t)
	sources[t] = article['source']
counters = Counter(titles)

for title in counters:
	if counters[title] > 1:
		print "["+sources[title]+"]["+str(counters[title])+"]", title.encode('utf-8')
