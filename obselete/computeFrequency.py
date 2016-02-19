import db
import time
import numpy as np

basic = 480

# UPDATE articles without a crawl frequency
# TODO: Document what this does.
feedUpdate = db.feed.initialize_unordered_bulk_op()

sourcesWithoutCrawlFreq = db.feed.find({'crawlFreq': {'$exists': False}})
for src in sourcesWithoutCrawlFreq:
	feedUpdate.find({'feed': src['feed']}).upsert().update({'$set': {'crawlFreq': basic}})

# UPDATE articles with a crawl frequency

match = {'$match': {'timestamp': {'$gte': time.time()-30*86400}}}
sort = {'$sort': {'timestamp': 1}}
group = {'$group': {'_id': '$feed', 'tsVec': {'$push': '$timestamp'}, 'count': {'$sum': 1}}}
for d in db.aggregateArticles([match, sort, group], shouldYield=True):
	updateFrequency = basic # By default: update every 8 minutes
	if d['count'] > 1:
		diffVec = np.diff(d['tsVec'])
		updateFrequency = np.percentile(diffVec, 10) # We want to get 90% of the cases considered
	updateFrequency = int(min(max(updateFrequency, 120), 3600)) # update at most every 2 minutes, at least once per hour
	feedUpdate.find({'feed': d['_id']}).upsert().update({'$set': {'crawlFreq': updateFrequency}})

feedUpdate.execute()
