# -*- coding: utf-8 -*-
from dbco import *
from article import *
from crawlContent import *
import sys

# articles = db.qdoc.find({'content': ''})

# for a in articles:
# 	art = [Article('blabla', a['title'], a['url'], 1431243710, a['source'], "cnn_world")]
# 	art = crawlContent(art)
# 	new_cont = art[0].content
# 	db.qdoc.update({'guid': a['guid']}, {'$set': {'content': new_cont}}, multi=True)
# 	print "Done"



source = sys.argv[1]
ski = int(sys.argv[2])
a = db.qdoc.find({'$query': {'source': source}, '$orderby': {'timestamp': -1}}).limit(1).skip(ski)
a = db.qdoc.find({'$query': {'keywords': 'print'}, '$orderby': {'timestamp': -1}}).limit(1).skip(ski)
a = a[0]
art = [Article(a['_id'], a['title'], a['url'], a['timestamp'], a['source'], a['feed'])]
art = crawlContent(art)

with open("new_content.txt", "w") as f:
	f.write(art[0].content)
with open("old_content.txt", "w") as f:
	f.write(a['content'].encode('utf-8'))

print "Done"
