from dbco import *
from article import *
from crawlContent import *

articles = db.qdoc.find({'content': ''}).limit(20)

for a in articles:
	art = [Article('blabla', a['title'], a['url'], 1431243710, a['source'], "cnn_world")]
	art = crawlContent(art)
	new_cont = art[0].content
	db.qdoc.update({'guid': a['guid']}, {'$set': {'content': new_cont}}, multi=True)
	print "Done"