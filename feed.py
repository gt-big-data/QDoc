"""This file represents a single RSS feed throughout the lifecycle of a feed.

This feed may be invalid, uncrawlable, recently crawled, soon-to-be crawled, or in any state.

As long as there's a URL pointing to something that we think is an RSS feed, there can be a feed object.
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime

NO_ARTICLES_FOUND = 'NO_ARTICLES_FOUND'
PARSE_FEED_ITEM_FAILED = 'PARSE_FEED_ITEM_FAILED'

class Feed(object):
    def __init__(self, url, html='', articles=None):
        # Expecting most Feed objects to just be initialized with a URL.
        self.url = url
        self.originalUrl = url
        self.html = html
        self.articles = articles or None

    def downloadFeed(self):
        try:
            response = requests.get(self.url, timeout=5)
        except Exception as e:
            print 'Could not download the feed: %s' % self.url
            print e
            return False
        self.html = response.text
        self.url = response.url # URL may have been redirected or slightly modified during the request.
        return True

    def save(self):
        db.feed.update({'feed': self.originalUrl}, {'$set': {
            'feed': self.url
            'stamp': int(latestStamp),
            'lastCrawl': self.lastCrawlTime
        }}, upsert=True)

    def disable(self, reason):
        db.feed.update({'feed': self.originalUrl}, {'$set': {
            'active': False,
            'disableReason': reason
        }})

    def parseFeed(self):
        if len(self.html) == 0:
            print "No HTML present. Not attempting to parse."
            return

        soup = BeautifulSoup(self.html)
        if len(self.articles) > 0:
            print 'WARNING: Recrawling a feed with existing articles.'
            print 'Number of existing articles: %d' % len(self.articles)
        self.articles = [] # In the event that articles have already been crawled, clear it anyways.

        # Each one of these has the HTML containing a link to an article and probably some basic information.
        feedItems = soup.find_all(['item', 'entry'])
        if len(items) == 0:
            print "Could not find any articles in the feed: %s" % self.url
            print "Please disable the feed because it requires manual inspection."
            return NO_ARTICLES_FOUND

        for item in feedItems:
            article = feedItemToArticle(item)
            if article is None:
                print "Could not create an article from the given item:"
                print item
                continue
            article.feed = self.url
            self.articles.append(article)
        self.lastCrawlTime = datetime.utcnow()
