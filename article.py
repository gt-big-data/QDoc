# TODO: Grab this from a config file.
from writers import *
from isDuplicate import *
writer = MongoWriter()

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
        self.content = content
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

    def save(self):
        """Write this article to the preferred method of writing.
        This method will print out an error if the article is not valid.
        """
        dupID = isDuplicate(self.content, self.source)
        if not self.isValid():
            print("Article from source: " + self.source + "feed: " + self.feed + " was invalid")
        elif dupID is not None: # we just update the content because this is a duplicate of something
            writer.updateDuplicate(dupID, self)
        else: # Write full on article
            writer.write(self)
