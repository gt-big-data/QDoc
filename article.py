# TODO: Grab this from a config file.
from writers import MongoWriter
writer = MongoWriter()

def good(val):
    return val and len(val) > 0

class Article(object):
    def __new__(self, guid='', title='', url='', timestamp=0, source='', feed=''):
        self.guid = guid
        self.title = title
        self.url = url
        self.timestamp = timestamp
        self.source = source
        self.feed = feed
        self.content = ''
        self.img = ''
        self.keywords = []

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

def saveNewArticles(newArticles):
    """Add valid articles to the database."""
    for article in newArticles:
        if a.isValid():
            writer.write(article)
        else:
            print("Article from source: " + a.source + "feed: " + a.feed + " was invalid")
