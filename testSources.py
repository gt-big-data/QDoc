import warnings
from dbco import *
from utils import downloader
from urlparse import urljoin
from bson import ObjectId
from crawlFeed import *
import time

warnings.filterwarnings("ignore")

# STEP 1: See if an RSS feed is available
while db.test_sources.find({'tested': {'$exists': False}}).count() > 0:
	sources = list(db.test_sources.find({'tested': {'$exists': False}}).limit(50))
	sourceUpdate = db.test_sources.initialize_unordered_bulk_op()
	results = downloader.getUrls([src['source'] for src in sources])
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
print "Done with STEP 1"

# STEP 2: See if the format is right
while db.test_sources.find({'rss': {'$exists': True}, 'validFormat': {'$exists': False}, 'formatError': {'$exists': False}}).count() > 0:
	sources = list(db.test_sources.find({'rss': {'$exists': True}, 'validFormat': {'$exists': False}, 'formatError': {'$exists': False}}).limit(50)) # a little yolo
	results = downloader.getUrls([src['rss'] for src in sources])
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
print "Done with STEP 2"

# STEP 3: Add them as inactive sources to the main thread

alreadySource = set([s['feed'] for s in list(db.feed.find({}, {'feed': 1}))]) # can't find a better way to do this
feedUpdate = db.feed.initialize_unordered_bulk_op(); any = False
for src in db.test_sources.find({'validFormat': {'$exists': True}}):
	if src['rss'] not in alreadySource:
		any = True
		feedUpdate.find({'feed': src['rss']}).upsert().update({'$set': {'feed': src['rss'], 'active': False, 'crawlFreq': 240, 'lastCrawl': int(time.time()-240)}})
if any:
	feedUpdate.execute()
print "Done with STEP 3"

# feedUpdate = db.feed.initialize_unordered_bulk_op()
# feeds = db.feed.find({'active': False}).limit(300)
# for f in feeds:
# 	feedUpdate.find({'feed': f['feed']}).upsert().update({'$set': {'active': True}})
# feedUpdate.execute()
