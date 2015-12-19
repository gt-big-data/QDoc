from bson.objectid import ObjectId
from crawlContent import *
from article import *
from dbco import *
import sys, socket, eventlet
from eventlet.green import urllib2
socket.setdefaulttimeout(5)

def recrawlArt(art):
	try:
		html = urllib2.urlopen(art['url']).read()
	except:
		print "Error 404: Not Found"
		return {'id': art['_id'], 'content': None}

	article = Article(guid=art['guid'], title=art['title'], url=art['url'], timestamp=art['timestamp'], source=art['source'], feed=art['feed'])
	soup = htmlToSoup(article, html)
	parse(article, html)

	cleanHTML = soup.prettify().encode('utf8')

	oldContent = art.get('content', '').encode('utf8')
	newContent = article.content.encode('utf8')
	print "-------------------------"
	print art['_id']
	print "Old: ", len(oldContent), " | New: ", len(newContent)
	return {'id': art['_id'], 'content': newContent}

def recrawlSource(source=None):
	left = db.qdoc.find({'recrawl': {'$exists': True}}).count()
	while left>0:
		sort = -1
		articles = list(db.qdoc.find({'recrawl': {'$exists': True}}).sort('timestamp', sort).limit(50))

		qdocUpdate = db.qdoc.initialize_unordered_bulk_op()

		batch = []
		i = 0
		while i < len(articles):
			while len(batch) < min(20, left):
				batch.append(articles[i])
				i += 1

			pool = eventlet.GreenPool()

			for ret in pool.imap(recrawlArt, batch):
				if ret['content']:
					print len(ret['content'])
					qdocUpdate.find({'_id': ret['id']}).upsert().update({'$set': {'content': ret['content']}, '$unset': {'recrawl': True}})
				else:
					qdocUpdate.find({'_id': ret['id']}).upsert().update({'$unset': {'recrawl': True}})
			left -= len(batch)
			batch = []

		qdocUpdate.execute()
		left = db.qdoc.find({'recrawl': {'$exists': True}}).count()
		print "-------------------------------------"		
		print "-------------------------------------"		
		print "Left: ", left

recrawlSource()