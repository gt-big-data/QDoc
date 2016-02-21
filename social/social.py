import time, datetime, fb
from dbco import *
from datetime import timedelta as td

def getAggregate():
	dtnow = datetime.datetime.now()
	longAgo = dtnow - td(days=8)
	hoursAfterFetch = [1, 2, 4, 6, 12, 18, 24, 48, 72, 96, 168]
	match = {'$match': {'timestamp': {'$gte': longAgo}}} # limit the scope to recent articles
	proj = {'$project': {'title': 1, 'url': 1, 'numFetches': {'$size': { "$ifNull": [ "$social", [] ] }}, 'timestamp': 1, 'lastSocial': {'$ifNull': [{'$max': '$social.date'}, longAgo]}}}
	match2 = {'$match': {'lastSocial': {'$lte': dtnow - td(hours=1)}}} # Haven't crawled it in 1 hour
	ors = [{'timestamp': {'$lte': dtnow-td(hours=t)}, 'numFetches': {'$lte': c}} for c, t in zip(range(len(hoursAfterFetch)), hoursAfterFetch)]
	match3 = {'$match': {'$or': ors}}
	limit = {'$limit': 100}
	return list(db.qdoc.aggregate([match, proj, match2, match3, limit]))

arts = getAggregate()
waves = 0
while len(arts) > 0:
	qdocUpdate = db.qdoc.initialize_unordered_bulk_op()
	urls = [a['url'] for a in arts]
	fbRet = fb.url_counts(urls)
	# print fbRet
	for art in arts:
		thisFb = fbRet.get(art['url'], 0)
		qdocUpdate.find({'_id': art['_id']}).upsert().update({'$push': {'social': {'date': datetime.datetime.now(), 'fb': thisFb}}})
	waves += 1
	print waves
	if waves > 20:
		break
	qdocUpdate.execute()
	arts = getAggregate()