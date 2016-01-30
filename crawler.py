from crawlFeed import *
from getUrl import *
import time

start_time = time.time()

feedList = list(db.feed.find({'active': True})) # this gets the list of feeds

i=0
while i < len(feedList):
	tempSize = min(50, (len(feedList)-i))
	tempList = feedList[i:(i+tempSize)]
	results = getURLs([f['feed'] for f in tempList])
	for res, feed in zip(results, tempList):
		crawlFeed(feed['feed'], res, feed['stamp'])
	i += tempSize
print("--- %s seconds ---" % round(time.time() - start_time, 2))