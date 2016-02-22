from datetime import datetime

from feed import Feed, downloadFeeds, parseFeeds, downloadArticlesInFeeds
from utils import ip
from article import Article, parseArticles
import db, time

startTime = datetime.utcnow()

match = {'$match': {'active': True}}
project = {'$project': {'milliSecondsUntilRedo': {'$subtract': [{'$subtract': [startTime, '$lastCrawl']}, {'$multiply': [1000, '$crawlFreq']}]}, 'feed': 1, 'stamp': 1, 'lastCrawl': 1, 'active': 1}} # Substracting datetime and a number of seconds doesn't work
match2 = {'$match': {'milliSecondsUntilRedo': {'$gte': 0}}} # only get the ones that must be redone
sort = {'$sort': {'milliSecondsUntilRedo': -1}} # most important ones first
limit = {'$limit': 150} # we only get the 150 most pressing sources :)

feedList = db.aggregateFeeds([match, project, match2, sort, limit])

newArticlesCount = 0
duplicateArticlesCount = 0
validArticlesCount = 0
feedsCount = 0

i = 0
newArticles = []
batchSize = 50
while i < len(feedList):
	tempList = feedList[i:(i + batchSize)]
	feeds = [Feed(url=feed['feed'], stamp=feed.get('stamp', None)) for feed in tempList]
	feeds = downloadFeeds(feeds)
	feeds = parseFeeds(feeds)
	feeds = downloadArticlesInFeeds(feeds)
	newArticles = []
	for feed in feeds:
		newArticles.extend(feed.articles)
	newArticles = parseArticles(newArticles)
	validArticles = [article for article in newArticles if article.isValid()]
	duplicateArticlesC = [article.save() for article in validArticles].count(True)
	for feed in feeds:
		print '%s => +%d' % (feed.url, len(feed.articles))
		feed.save()
	i += batchSize

	newArticlesCount += len(newArticles)
	duplicateArticlesCount += duplicateArticlesC
	validArticlesCount += len(validArticles)
	feedsCount += len(feeds)

endTime = datetime.utcnow()
runTime = round((endTime - startTime).total_seconds(), 2)
db.log({
	'startTime': startTime,
	'runTime': runTime,
	'ip': ip.get_ip_address(),
	'feeds': feedsCount,
	'newArticles': newArticlesCount,
	'duplicateArticles': duplicateArticlesCount,
	'validArticles': validArticlesCount
})
print("--- %s seconds ---" % runTime)
