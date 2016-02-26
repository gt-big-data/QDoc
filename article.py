import concurrent.futures as futures # for multithreading
import requests

from utils import articleQa, articleParser
import db

from config import config

def good(val):
    return val and len(val) > 0

class Article(object):
    def __init__(self, guid='', title='', url='', html='', timestamp=None, source='', feed='', content=''):
        self.guid = guid
        self.title = title.encode('utf-8').strip()
        self.url = url.decode('utf-8').strip()
        self.timestamp = timestamp
        self.source = source.decode('utf-8')
        self.feed = feed.decode('utf-8')
        self.content = content.decode('utf-8').strip()
        self.keywords = []
        self.html = html.decode('utf-8')

    def isDuplicate(self):
        return articleQa.isDuplicate(self)

    def downloadArticle(self):
        try:
            response = requests.get(self.url, timeout=5)
        except Exception as e:
            print 'Could not download the article: %s' % self.url
            print e
            return False
        self.url = response.url # Could have changed during redirects.
        self.html = response.text.replace('<br>', '<br />') # the replace is important, don't omit
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

def parseArticles(articles, maxWorkers=config['parseWorkers']):
    print 'Parsing %d article(s) with %d process(es).' % (len(articles), maxWorkers)
    with futures.ProcessPoolExecutor(max_workers=maxWorkers) as executor:
        articlesFutures = executor.map(_parse, articles)
        # Force the futures generator to give us all of the articles back.
        articles = [article for article in articlesFutures]
    return articles
