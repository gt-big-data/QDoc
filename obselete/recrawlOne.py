# TODO: This script is definitely broken. Either salvage it or delete it.

from crawlContent import *
from article import Article
import db
import sys

# This file can help testing the crawling of a given ID: it'll produce the HTML, the old content and the new content (for comparison)
def recrawlTest(art):
	art = db.getArticleById(id))
	art['url'] = art['url'].split('?')[0]
	html = urllib2.urlopen(art['url']).read()
	article = Article(guid=art['guid'], title=art['title'], url=art['url'], timestamp=art['timestamp'], source=art['source'], feed=art['feed'])

	header = art['source']+" - "+str(art['_id'])+"\n----------------------------------------------\n\n"
	soup = htmlToSoup(article, html)
	parse(article, html)

	f = open('totalCrawl.html', 'w'); f.write(html); f.close();
	f = open('latestCrawl.html', 'w'); f.write(soup.prettify().encode('utf-8')); f.close();
	f = open('oldContent.txt', 'w'); f.write((header+art['content']).encode('utf-8')); f.close();
	f = open('newContent.txt', 'w'); f.write((header+article.content).encode('utf-8')); f.close();

	print article.url

if __name__ == '__main__':
	if len(sys.argv) > 1:
		art = db.getArticleById(sys.argv[1])
	else:
		art = db.getRandomRecentArticle()
	recrawlTest(art)
