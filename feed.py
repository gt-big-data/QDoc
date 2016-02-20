"""This file represents a single RSS feed throughout the lifecycle of a feed.

This feed may be invalid, uncrawlable, recently crawled, soon-to-be crawled, or in any state.

As long as there's a URL pointing to something that we think is an RSS feed, there can be a feed object.
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import concurrent.futures as futures # for multithreading
import db

from feedItem import feedItemToArticle

NO_ARTICLES_FOUND = 'NO_ARTICLES_FOUND'
PARSE_FEED_ITEM_FAILED = 'PARSE_FEED_ITEM_FAILED'
NO_HTML_FOUND = 'NO_HTML_FOUND'

class Feed(object):
    def __init__(self, url, stamp=None, html='', articles=None):
        # Expecting most Feed objects to just be initialized with a URL and stamp.
        self.url = url
        self.originalUrl = url
        self.lastTimeStamp = stamp or datetime(1970, 1, 1, 0, 0, 0)
        self.lastTimeStamp = self.lastTimeStamp.replace(tzinfo=pytz.utc)
        self.html = html
        self.articles = articles or None
        self.lastCrawlTime = None

    def downloadFeed(self):
        try:
            response = requests.get(self.url, timeout=5)
            if response.status_code == 404:
                raise Exception('404 - Could not find a feed at the given address.')
        except Exception as e:
            print 'Could not download the feed: %s' % self.url
            print e
            return False
        self.lastCrawlTime = datetime.utcnow()
        self.html = response.text
        self.url = response.url # URL may have been redirected or slightly modified during the request.
        return True

    def save(self):
        if self.lastCrawlTime is None:
            print 'Cannot save a feed before crawling it. Doing nothing.'
            return
        print 'Saving feed %s (stamp: %s, lastCrawl: %s)' % (self.url, self.lastCrawlTime.strftime('%c'), self.lastTimeStamp.strftime('%c'))
        db.feed.update({'feed': self.originalUrl}, {'$set': {
            'feed': self.url,
            'stamp': self.lastTimeStamp,
            'lastCrawl': self.lastCrawlTime
        }}, upsert=True)

    def disable(self, reason):
        db.feed.update({'feed': self.originalUrl}, {'$set': {
            'active': False,
            'disableReason': reason
        }})

    def parseFeed(self):
        """
        Return tuple of (err, metadata) where err is a semi-generic string if an error occurred or None.
        metadata is a dict of a few statistics about the articles that were found or None if an error occured.
        """
        self.lastCrawlTime = datetime.utcnow()
        if self.articles is not None and len(self.articles) > 0:
            print 'WARNING: Recrawling a feed with existing articles.'
            print 'Number of existing articles: %d' % len(self.articles)
        self.articles = [] # In the event that articles have already been crawled, clear it anyways.

        if len(self.html) == 0:
            print "No HTML present. Not attempting to parse."
            return NO_HTML_FOUND, None

        soup = BeautifulSoup(self.html, 'html.parser')

        # Each one of these has the HTML containing a link to an article and probably some basic information.
        feedItems = soup.find_all(['item', 'entry'])
        if len(feedItems) == 0:
            print "Could not find any articles in the feed: %s" % self.url
            print "Please disable the feed because it requires manual inspection."
            return NO_ARTICLES_FOUND, None

        articleStats = {
            'foundArticles': len(feedItems),
            'newArticles': 0,
            'invalidArticles': 0
        }

        for item in feedItems:
            article = feedItemToArticle(item)
            if article is None:
                print "Could not create an article from the given item:"
                print item
                articleStats['invalidArticles'] += 1
                continue
            elif article.timestamp < self.lastTimeStamp:
                print 'Got to end of the feed.'
                break
            articleStats['newArticles'] += 1
            article.feed = self.url
            self.articles.append(article)
        stamps = [self.lastTimeStamp] + [article.timestamp for article in self.articles]
        self.lastTimeStamp = max(stamps)
        return None, articleStats

def _download(feed):
    feed.downloadFeed()
    return feed

def downloadFeeds(feeds, maxWorkers=100):
    print 'Downloading %d feeds with %d threads.' % (len(feeds), maxWorkers)
    with futures.ThreadPoolExecutor(max_workers=maxWorkers) as executor:
        feedFutures = executor.map(_download, feeds)
        feeds = [feed for feed in feedFutures]
    return feeds

def _parse(feed):
    feed.parseFeed()
    return feed

def parseFeeds(feeds):
    # Not threading because GIL would make the efforts worthless.
    # Not using processes because the total amount of work here is very small.
    print 'Parsing %d feeds.' % (len(feeds))
    for feed in feeds:
        print 'Parsing %s' % feed.url
        feed.parseFeed()
    return feeds

def _downloadArticles(feed):
    # Sequentially download every article in a feed.
    # Prevents us from causing excessive load to any single source.
    for article in feed.articles:
        article.downloadArticle()
    return feed

def downloadArticlesInFeeds(feeds, maxWorkers=4):
    print 'Downloading articles from %d feeds with %d threads.' % (len(feeds), maxWorkers)
    with futures.ThreadPoolExecutor(max_workers=maxWorkers) as executor:
        feedFutures = executor.map(_downloadArticles, feeds)
        feeds = [feed for feed in feedFutures]
    return feeds
