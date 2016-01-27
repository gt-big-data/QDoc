from crawlFeed import *
import time, eventlet

start_time = time.time()

feedList = list(db.feed.find({'active': True})) # this gets the list of feeds

requests = eventlet.import_patched('requests.__init__')

def prepareCrawlfeed(feed):
	crawlFeed(feed['feed'], feed['stamp'], requests)

pool = eventlet.GreenPool()
i=0
while i < len(feedList):
	tempSize = min(50, (len(feedList)-i))
	tempList = feedList[i:(i+tempSize)]
	for ret in pool.imap(prepareCrawlfeed, tempList):
		pass
	i += tempSize
print("--- %s seconds ---" % round(time.time() - start_time, 2))