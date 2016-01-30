import warnings
from dbco import *
from getUrl import *
from urlparse import urljoin
from bson import ObjectId
from crawlFeed import *

warnings.filterwarnings("ignore")

# STEP 1: See if an RSS feed is available
while db.test_sources.find({'tested': {'$exists': False}}).count() > 0:
	sources = list(db.test_sources.find({'tested': {'$exists': False}}).limit(50))
	sourceUpdate = db.test_sources.initialize_unordered_bulk_op()
	results = getURLs([src['source'] for src in sources])
	for res, src in zip(results, sources):
		toSet = {'tested': src.get('tested', 0)+1}
		if 'error' in res:
			toSet['error'] = res['error']
		link = res['soup'].find('link', type='application/rss+xml')
		if link is not None and len(link.get('href','')) > 0:
			toSet['rss'] = urljoin(src['source'], link.get('href'))
			print toSet['rss']

		sourceUpdate.find({'source': src['source']}).upsert().update({'$set': toSet})

	sourceUpdate.execute()

# STEP 2: See if the format is right
while db.test_sources.find({'rss': {'$exists': True}, 'validFormat': {'$exists': False}, 'formatError': {'$exists': False}}).count() > 0:
	sources = list(db.test_sources.find({'rss': {'$exists': True}, 'validFormat': {'$exists': False}, 'formatError': {'$exists': False}}).limit(50)) # a little yolo
	results = getURLs([src['rss'] for src in sources])
	sourceUpdate = db.test_sources.initialize_unordered_bulk_op()
	for src, res in zip(sources, results):
		ret = crawlFeed(src['rss'], res, 0, False)
		toSet = {}
		if len(ret) == 0: # noError
			toSet['validFormat'] = True
		else:
			toSet['formatError'] = ret
		sourceUpdate.find({'source': src['source']}).upsert().update({'$set': toSet})

	sourceUpdate.execute()
	print db.test_sources.find({'rss': {'$exists': True}, 'validFormat': {'$exists': False}, 'formatError': {'$exists': False}}).count(), "left"