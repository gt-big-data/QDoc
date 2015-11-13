from bson.objectid import ObjectId
from crawlContent import *
from article import *
from dbco import *
import sys

# This file can help testing the crawling of a given ID: it'll produce the HTML, the old content and the new content (for comparison)
if len(sys.argv) > 1:
	idT = sys.argv[1]
	art = list(db.qdoc.find({'_id': ObjectId(idT)}).limit(1))[0]
	art['url'] = art['url'].split('?')[0]
	html = urllib2.urlopen(art['url']).read()
	article = Article(guid=art['guid'], title=art['title'], url=art['url'], timestamp=art['timestamp'], source=art['source'], feed=art['feed'])

	soup = htmlToSoup(article, html)
	parse(article, html)
	f = open('latestCrawl.html', 'w'); f.write(soup.prettify().encode('utf8')); f.close();
	f = open('oldContent.txt', 'w'); f.write(art['content'].encode('utf8')); f.close();
	f = open('newContent.txt', 'w'); f.write(article.content.encode('utf8')); f.close();

	print article.url