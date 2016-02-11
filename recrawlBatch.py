from bson.objectid import ObjectId
from crawlContent import *
from dbco import *
from getUrl import *
import sys, socket, random
socket.setdefaulttimeout(5)

def recrawlArt(art,urlReturn):

	urlReturn = getUrl(art['url'])
	if 'error' in urlReturn:
		print 'Error', urlReturn['error'], 'in article', art['_id']
		return None

	soup = urlReturn['soup']

	cleanHTML = soup.prettify().encode('utf8')

	oldContent = art.get('content', '').encode('utf8')
	newContent = getContent(soup, art['source']).encode('utf8')
	print art['_id'], " | Old: "+ str(len(oldContent)).center(5)+ " | New: "+str(len(newContent)).center(5)
	return {'id': art['_id'], 'content': newContent}

def recrawlSource():
	left = db.qdoc.find({'recrawl': {'$exists': True}}).count()
	while left>0:
		rand = int(2000*random.random())
		any = False
		match = {'$match': {'recrawl': {'$exists': True}}}
		project = {'$project': {'_id': True, 'guid': True, 'title': True, 'url': True, 'feed': True, 'source': True, 'content': True, 'tsmod': {'$mod': ['$timestamp', rand]}}}
		sort = {'$sort': {'tsmod': -1}}
		limit = {'$limit': 30}

		articles = list(db.qdoc.aggregate([match, project, sort, limit]))

		qdocUpdate = db.qdoc.initialize_unordered_bulk_op()

		results = getURLs([a['url'] for a in articles])
		for res, art in zip(results, articles):
			ret = recrawlArt(art,res)
			if ret['content']:
				any = True
				qdocUpdate.find({'_id': ret['id']}).upsert().update({'$set': {'content': ret['content']}, '$unset': {'recrawl': True}})

		if any:
			qdocUpdate.execute()
		left = db.qdoc.find({'recrawl': {'$exists': True}}).count()
		print "-------------------------------------"		
		print "Left: ", left

recrawlSource()