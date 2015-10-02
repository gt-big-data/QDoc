import json
from dbco import * # this imports the db connection

def good(val):
    return val and len(val) > 0

class Article:
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
    As = []
    for a in newArticles:
        if a.isValid():
            As.append(a._asdict())
        else:
            print "Article from source: ", a.source, "feed: ", a.feed, " was invalid"
    if len(As) > 0:
        insertArticles(db, As)

# TODO : Move this into a writing interface (further away from Article).
def insertArticles(db, As):
    for a in As:
        db.qdoc.update({'guid': a['guid']}, {'$set': a}, upsert=True) # if the GUID is already in the set

# TODO: Move this into a writing interface (further away from Article).
def saveNewArticlesFile(newArticles):
    """Write an array of articles to DB_ex.txt"""
    with open("DB_ex.txt", "a") as f:
        for a in newArticles:
            if a.isValid():
                f.write(json.dumps(a._asdict())+'\n')
            else:
                print "Article from source: ", a.source, "feed: ", a.feed, " was invalid"
