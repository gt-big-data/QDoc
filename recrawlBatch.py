from bson.objectid import ObjectId
from crawlContent import *
from article import *
from dbco import *
import sys, socket
socket.setdefaulttimeout(5)

def recrawlArt(art, article):
	try:
		html = urllib2.urlopen(art['url']).read()
	except:
		print "Error 404: Not Found"
		return ""
	soup = htmlToSoup(article, html)
	parse(article, html)

	cleanHTML = soup.prettify().encode('utf8')
	oldContent = art['content'].encode('utf8')
	newContent = article.content.encode('utf8')
	print "-------------------------"
	print art['_id']
	print "Old: ", len(oldContent), " | New: ", len(newContent)
	return newContent

def recrawlSource(source=None):
	left = 1
	while left>0:
		sort = -1
		articles = list(db.qdoc.find({'recrawl': {'$exists': True}}).sort('timestamp', sort).limit(50))

		qdocUpdate = db.qdoc.initialize_unordered_bulk_op()
		for art in articles:
			article = Article(guid=art['guid'], title=art['title'], url=art['url'], timestamp=art['timestamp'], source=art['source'], feed=art['feed'])
			newContent = recrawlArt(art, article)
			if newContent:
				qdocUpdate.find({'_id': art['_id']}).upsert().update({'$set': {'content': newContent}, '$unset': {'recrawl': True}})
			else:
				qdocUpdate.find({'_id': art['_id']}).upsert().update({'$unset': {'recrawl': True}})

		qdocUpdate.execute()
		left = db.qdoc.find({'recrawl': {'$exists': True}}).count()
		print "-------------------------------------"		
		print "Left: ", left

recrawlSource()