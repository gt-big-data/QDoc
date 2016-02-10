from utils import articleQa
import db

def good(val):
    return val and len(val) > 0

class Article(object):
    def __init__(self, guid='', title='', url='', timestamp=0, source='', feed='', content=''):
        self.guid = guid
        self.title = title
        self.url = url
        self.timestamp = timestamp
        self.source = source
        self.feed = feed
        self.content = unicode(content)
        self.img = ''
        self.keywords = []

    def isDuplicate(self):
        return articleQa.isDuplicate(self)

    def isValid(self):
        """Check if the article has enough data to be considered "crawled"."""

        if not good(self.guid):
            return False
        if not good(self.title):
            return False
        if not good(self.url):
            return False
        if self.timestamp < 500:
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
        dupID = article_qa.isDuplicate(self)
        if not self.isValid():
            print("Article from source: " + self.source + "feed: " + self.feed + " was invalid")
        elif dupID is not None: # we just update the content because this is a duplicate of something
            db.updateArticle(dupID, self)
        else: # Write full on article
            db.insertArticle(self.guid, self)
        return dupID is not None
