import time
from datetime import datetime

from feed import Feed, downloadFeeds, parseFeeds
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

i = 0
newArticles = []
while i < len(feedList):
	tempList = feedList[i:(i + batchSize)]
	feeds = [Feed(url=feed['feed'], stamp=feed.get('stamp', 0)) for feed in tempList]
	feeds = downloadFeeds(feeds)
	feeds = parseFeeds(feeds)
	for feed in feeds:
		print '%s => +%d' % (feed.url, len(feed.articles))
		# TODO: Download and parse articles immediately.
		newArticles.extend(feed.articles)
		feed.save()
	i += batchSize

# TODO: Things are working up to here.
dupCount = 0
for a in newArticles:
	article = Article(**a)
	if not article.isValid():
		print("Article from source: " + a.get('source','') + "feed: " + a.get('feed','') + " was invalid")
		continue # skip bad articles
	dupID = article.isDuplicate()
	if dupID is not None: # Update duplicate
		db.updateArticle(dupID, {'content': a['content']})
		dupCount += 1
	else: # Write full on article
		db.insertArticle(a['guid'], a)

# TODO: Call feed.save() on all of the feeds.

crawl_time = datetime.now().isoformat()
db.log({'crawl_time': crawl_time, 'ip': ip.get_ip_address(), 'run_time': round(time.time() - start_time, 2), 'crawl_feeds': len(feedList), 'new_articles': len(newArticles), 'duplicate_count': dupCount})
print("--- %s seconds ---" % round(time.time() - start_time, 2))
