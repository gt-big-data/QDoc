# TODO: This script is definitely broken. Either salvage it or delete it.

from crawlContent import *
from article import Article
import db
import sys, random

# This file can help testing the crawling of a given ID: it'll produce the HTML, the old content and the new content (for comparison)
def recrawlTest(art):
	art = db.getArticleById(id))
	art['url'] = art['url'].split('?')[0]

	header = art['source']+" - "+str(art['_id'])+"\n----------------------------------------------\n\n"
	urlReturn = getUrl(art['url'])
	newContent = getContent(url['soup'], art['source'])

	f = open('latestCrawl.html', 'w'); f.write(urlReturn['soup'].prettify().encode('utf-8')); f.close();
	f = open('oldContent.txt', 'w'); f.write((header+art['content']).encode('utf-8')); f.close();
	f = open('newContent.txt', 'w'); f.write((header+newContent).encode('utf-8')); f.close();
	print art['url']

if __name__ == '__main__':
	if len(sys.argv) > 1:
		art = db.getArticleById(sys.argv[1])
	else:
		art = db.getRandomRecentArticle()
	recrawlTest(art)
