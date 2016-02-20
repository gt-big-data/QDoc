# -*- coding: utf-8 -*-
import concurrent.futures as futures # for multithreading
import requests

from utils import articleQa, articleParser
import db, sys

reload(sys)
sys.setdefaultencoding('utf8')

def good(val):
    return val and len(val) > 0

class Article(object):
    def __init__(self, guid='', title='', url='', html='', timestamp=None, source='', feed='', content=''):
        self.guid = guid
        self.title = title
        self.url = url
        self.timestamp = timestamp
        self.source = source
        self.feed = feed
        self.content = unicode(content)
        self.keywords = []
        self.html = html

    def isDuplicate(self):
        return articleQa.isDuplicate(self)

    def downloadArticle(self):
        try:
            response = requests.get(self.url, timeout=5)
        except Exception as e:
            print 'Could not download the article: %s' % self.url.encode('utf8')
            print e.encode('utf8')
            return False
        self.url = response.url # Could have changed during redirects.
        self.html = response.text
        return True

    def parseArticle(self):
        articleParser.parseArticle(self)

    def isValid(self):
        """Check if the article has enough data to be considered "crawled"."""

        if not good(self.guid):
            return False
        if not good(self.title):
            return False
        if not good(self.url):
            return False
        if self.timestamp is None:
            return False
        if not good(self.source):
            return False
        if not good(self.feed):
            return False
        if not good(self.content):
            return False
        return True

    def save(self):
        """Save the article to the database.
        This method will print out an error if the article is not valid.

        Return True if this is an original article and False if it's a duplicate.
        """
        dupID = articleQa.isDuplicate(self)
        if not self.isValid():
            print("Article from source: " + self.source + "feed: " + self.feed + " was invalid")
        elif dupID is not None: # we just update the content because this is a duplicate of something
            db.updateArticle(dupID, self)
        else: # Write full on article
            db.insertArticle(self.guid, self)
        return dupID is not None

def _parse(article):
    article.parseArticle()
    # No reason to keep this after parsing.
    # And deleting it here makes interprocess-pickling much faster.
    article.html = None
    return article

def parseArticles(articles, maxWorkers=4):
    print 'Parsing %d articles with %d processes.' % (len(articles), maxWorkers)
    with futures.ProcessPoolExecutor(max_workers=maxWorkers) as executor:
        articlesFutures = executor.map(_parse, articles)
        # Force the futures generator to give us all of the articles back.
        articles = [article for article in articlesFutures]
    return articles
