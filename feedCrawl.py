from urllib import urlopen
from bs4 import BeautifulSoup

from dateutil import parser
from datetime import datetime
import time
import pytz

from stamps import * # saving last stamps

from article import *
from crawlContent import *

def crawlFeed(source, feedName, feedUrl):
	# Given a feedname from a Source and a URL of where the Rss feed is,
	# Get the new articles, with their basic params: Title, URL, Publish Time
	startStamp = loadLastStamp(feedName)
	html = urlopen(feedUrl).read()
	epoch = datetime(1970, 1, 1).replace(tzinfo=pytz.utc)

	soup = BeautifulSoup(html, 'html.parser')
	latestStamp = startStamp
	newArticles = []

	for it in soup.find_all('item'):
		dt = extractPubTime(it)
		timestamp = (dt - epoch).total_seconds() # Hacky way of going from Datetime object to timestamp
		if timestamp > startStamp: # new article
			latestStamp = max(timestamp, latestStamp)
			url = extractLink(it)
			newArticles.append(Article(it.title.text, url, timestamp, source, feedName, '', ''))
		else:
			break # we're done, this assumes articles are ordered by descending pubDate

	newArticles = crawlContent(newArticles) # crawls for content, img and possible keywords (?)
	saveNewArticles(newArticles) # save to Database
	print feedName, " => +"+str(len(newArticles))

	saveLastStamp(feedName, latestStamp) # save to not reload articles

def extractPubTime(item):
	dt = parser.parse(item.pubdate.text) # string to Datetime
	return dt.replace(tzinfo=pytz.utc)

def extractLink(item):
	t1 = item.find('feedburner:origlink')
	t2 = item.find('link')
	if t1 is not None:
		return t1.text
	elif t2 is not None:
		return t2.text
	return ''