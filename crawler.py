from crawlFeed import *
from getUrl import *
import time, qa, datetime, ip

start_time = time.time()

match = {'$match': {'active': True}}
project = {'$project': {'secondsUntilRedo': {'$subtract': [{'$subtract': [int(time.time()), '$lastCrawl']}, '$crawlFreq']}, 'feed': 1, 'stamp': 1, 'lastCrawl': 1, 'active': 1}}
match2 = {'$match': {'secondsUntilRedo': {'$gte': 0}}} # only get the ones that must be redone
sort = {'$sort': {'secondsUntilRedo': -1}} # most important ones first
limit = {'$limit': 150} # we only get the 150 most pressing sources :)

feedList = list(db.feed.aggregate([match, project, match2, sort, limit]))

i=0
newArticles = []
while i < len(feedList):
	tempSize = min(50, (len(feedList)-i))
	tempList = feedList[i:(i+tempSize)]
	results = getURLs([f['feed'] for f in tempList])
	for res, feed in zip(results, tempList):
		feedReturn = crawlFeed(feed['feed'], res, feed.get('stamp',0))
		if type(feedReturn) is list:
			print feed['feed'], " => +"+str(len(feedReturn))
			newArticles.extend(feedReturn)
		else:
			print feed['feed'], "=>", feedReturn
	i += tempSize

crawlContent(newArticles)
dupCount = 0
for a in newArticles:
	if not qa.isValid(a):
		print("Article from source: " + a.get('source','') + "feed: " + a.get('feed','') + " was invalid")
		continue # skip bad articles
	dupID = qa.isDuplicate(a)
	if dupID is not None: # Update duplicate
		db.qdoc.update({'_id': dupID}, {'$set': {'content': a['content']}}) # update the content
		dupCount += 1
	else: # Write full on article
		db.qdoc.update({'guid': a['guid']}, {'$set': a}, upsert=True)

db.qdoc_log.insert_one({'crawl_time': datetime.datetime.now().isoformat(), 'ip': ip.get_ip_address(), 'run_time': round(time.time() - start_time, 2), 'crawl_feeds': len(feedList), 'new_articles': len(newArticles), 'duplicate_count': dupCount})
print("--- %s seconds ---" % round(time.time() - start_time, 2))