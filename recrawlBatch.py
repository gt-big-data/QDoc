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

	article = Article(guid=art['guid'], title=art['title'], url=art['url'], timestamp=0, source=art['source'], feed=art['feed'])
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
		rand = int(2000*random.random())
		any = False
		match = {'$match': {'recrawl': {'$exists': True}}}
		project = {'$project': {'_id': True, 'guid': True, 'url': True, 'feed': True, 'source': True, 'content': True, 'tsmod': {'$mod': ['$timestamp', rand]}}}
		sort = {'$sort': {'tsmod': -1}}
		limit = {'$limit': 30}

		articles = list(db.qdoc.aggregate([match, project, sort, limit]))

		qdocUpdate = db.qdoc.initialize_unordered_bulk_op()

		pool = eventlet.GreenPool()

		for ret in pool.imap(recrawlArt, articles):
			if ret['content']:
				any = True
				qdocUpdate.find({'_id': ret['id']}).upsert().update({'$set': {'content': ret['content']}, '$unset': {'recrawl': True}})
			# else: # for now we redo ...
			# 	qdocUpdate.find({'_id': ret['id']}).upsert().update({'$unset': {'recrawl': True}})

		if any:
			qdocUpdate.execute()
		left = db.qdoc.find({'recrawl': {'$exists': True}}).count()
		print "-------------------------------------"		
		print "-------------------------------------"		
		print "Left: ", left

recrawlSource()