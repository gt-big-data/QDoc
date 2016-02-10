import time, datetime

from crawlFeed import *
from utils import ip, downloader
from article import Article
import db

start_time = time.time()

match = {'$match': {'active': True}}
project = {'$project': {'secondsUntilRedo': {'$subtract': [{'$subtract': [int(time.time()), '$lastCrawl']}, '$crawlFreq']}, 'feed': 1, 'stamp': 1, 'lastCrawl': 1, 'active': 1}}
match2 = {'$match': {'secondsUntilRedo': {'$gte': 0}}} # only get the ones that must be redone
sort = {'$sort': {'secondsUntilRedo': -1}} # most important ones first
limit = {'$limit': 150} # we only get the 150 most pressing sources :)

feedList = db.aggregateFeeds([match, project, match2, sort, limit])

i=0
newArticles = []
while i < len(feedList):
	tempSize = min(50, (len(feedList)-i))
	tempList = feedList[i:(i+tempSize)]
	results = downloader.getUrls([f['feed'] for f in tempList])
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
	article = Article(a)
	if not Article(a).isValid():
		print("Article from source: " + a.get('source','') + "feed: " + a.get('feed','') + " was invalid")
		continue # skip bad articles
	dupID = a.isDuplicate()
	if dupID is not None: # Update duplicate
		db.updateArticle(dupID, {'content': a['content']})
		dupCount += 1
	else: # Write full on article
		db.insertArticle(a['guid'], a)

db.log({'crawl_time': datetime.datetime.now().isoformat(), 'ip': ip.get_ip_address(), 'run_time': round(time.time() - start_time, 2), 'crawl_feeds': len(feedList), 'new_articles': len(newArticles), 'duplicate_count': dupCount})
print("--- %s seconds ---" % round(time.time() - start_time, 2))
