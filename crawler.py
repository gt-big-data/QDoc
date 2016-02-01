from crawlFeed import *
from getUrl import *
import time

start_time = time.time()

match = {'$match': {'active': True}}
project = {'$project': {'secondsUntilRedo': {'$subtract': [{'$subtract': [int(time.time()), '$lastCrawl']}, '$crawlFreq']}, 'feed': 1, 'stamp': 1, 'lastCrawl': 1, 'active': 1}}
match2 = {'$match': {'secondsUntilRedo': {'$gte': 0}}} # only get the ones that must be redone
sort = {'$sort': {'secondsUntilRedo': -1}} # most important ones first
limit = {'$limit': 150} # we only get the 500 most pressing sources :)

feedList = list(db.feed.aggregate([match, project, match2, sort, limit]))

i=0
while i < len(feedList):
	tempSize = min(50, (len(feedList)-i))
	tempList = feedList[i:(i+tempSize)]
	results = getURLs([f['feed'] for f in tempList])
	for res, feed in zip(results, tempList):
		crawlFeed(feed['feed'], res, feed.get('stamp',0))
	i += tempSize
print("--- %s seconds ---" % round(time.time() - start_time, 2))