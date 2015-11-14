from bson.objectid import ObjectId
from crawlContent import *
from article import *
from dbco import *
import sys

def recrawlArt(art, article):
	try:
		html = urllib2.urlopen(art['url']).read()
	except:
		print "Error 404: Not Found"
		return None
	soup = htmlToSoup(article, html)
	parse(article, html)

	cleanHTML = soup.prettify().encode('utf8')
	oldContent = art['content'].encode('utf8')
	newContent = article.content.encode('utf8')
	# f = open('latestCrawl.html', 'w'); f.write(cleanHTML); f.close();
	# f = open('oldContent.txt', 'w'); f.write(oldContent); f.close();
	# f = open('newContent.txt', 'w'); f.write(newContent); f.close();
	print "-------------------------"
	print art['_id']
	print "Old: ", len(oldContent), " | New: ", len(newContent)
	return newContent

def recrawlSource(source):
	left = 1
	while left>0:
		sort = -1;
		articles = list(db.qdoc.find({'source': source, 'recrawled': {'$exists': False}}).sort('timestamp', sort).limit(50))

		qdocUpdate = db.qdoc.initialize_unordered_bulk_op()
		for art in articles:
			article = Article(guid=art['guid'], title=art['title'], url=art['url'], timestamp=art['timestamp'], source=art['source'], feed=art['feed'])
			newContent = recrawlArt(art, article)
			if newContent:
				qdocUpdate.find({'_id': art['_id']}).upsert().update({
					'$set': {'recrawled': True,	'content': newContent,}
				})
		qdocUpdate.execute()
		left = db.qdoc.find({'source': source, 'recrawled': {'$exists': False}}).count()
		print "-------------------------------------"		
		print "-------------------------------------"		
		print "Left: ", left

recrawlSource('guardian')
