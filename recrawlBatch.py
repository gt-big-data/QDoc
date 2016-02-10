from crawlContent import *
from article import Article
import db
import sys, socket
from utils import downloader

# TODO: This script has heavily refactored and is still untested. Proceed with caution.
# TODO: Do we still need this.
socket.setdefaulttimeout(5)



def recrawlArt(art, urlReturn):
	article = Article(**art)

	urlReturn = downloader.getUrl(art['url'])
	if 'error' in urlReturn:
		print 'Error', urlReturn['error'], 'in article', art['_id']
		break
	soup =
	crawlContent([article])

	cleanHTML = soup.prettify().encode('utf8')

	oldContent = art.get('content', '').encode('utf8')
	newContent = article.content.encode('utf8')
	print art['_id'], " | Old: "+ str(len(oldContent)).center(5)+ " | New: "+str(len(newContent)).center(5)
	return {'id': art['_id'], 'content': newContent}

def recrawlSource():
	left = db.countArticles({'recrawl': {'$exists': True}})
	while left > 0:
		rand = int(2000*random.random())
		any = False
		match = {'$match': {'recrawl': {'$exists': True}}}
		project = {'$project': {'_id': True, 'guid': True, 'title': True, 'url': True, 'feed': True, 'source': True, 'content': True, 'tsmod': {'$mod': ['$timestamp', rand]}}}
		sort = {'$sort': {'tsmod': -1}}
		limit = {'$limit': 30}

		articles = db.aggregateArticles([match, project, sort, limit])

		results = downloader.getUrls([a['url'] for a in articles])
		def bulkUpdater(updater):
			for res, art in zip(results, articles):
				ret = recrawlArt(art, res)
				if ret['content']:
					updater({'_id': ret['id']}, {'$set': {'content': ret['content']}, '$unset': {'recrawl': True}})
		db.bulkUpdateArticles(bulkUpdater)

		left = db.countArticles({'recrawl': {'$exists': True}})
		print "-------------------------------------"
		print "Left: ", left

recrawlSource()
