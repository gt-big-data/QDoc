from collections import Counter
from dbco import *

articles = db.qdoc.find()

titles = []
sources = {}
i = 1
for article in articles:
	t = article['title']
	titles.append(t)
	sources[t] = article['source']
	print i
	i += 1
counters = Counter(titles)

for title in counters:
	if counters[title] >= 1:
		print "["+sources[title]+"]["+str(counters[title])+"]", title.encode('utf-8')