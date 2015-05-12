from collections import namedtuple
import json
import dbco

Article = namedtuple('Article', ['title', 'url', 'timestamp', 'source', 'feed', 'content', 'img', 'keywords'])
class Article(namedtuple('Article', ['title', 'url', 'timestamp', 'source', 'feed', 'content', 'img', 'keywords'])):
    def __new__(cls, title='', url='', timestamp=0, source='', feed='', content='CC', img='', keywords=[]):
        return super(Article, cls).__new__(cls, title, url, timestamp, source, feed, content, img, keywords)

def saveNewArticles(newArticles):

	As = []
	for a in newArticles:
		if isValid(a):
			As.append(a._asdict())
		else:
			print "Article from source: ", a.source, "feed: ", a.feed, " was invalid"
	if len(As) > 0:
		insertArticles(db, As)

def insertArticles(db, As):
	db.qdoc.insert(As)

def saveNewArticlesFile(newArticles):
	with open("DB_ex.txt", "a") as f:
		for a in newArticles:
			if isValid(a):
				f.write(json.dumps(a._asdict())+'\n')
			else:
				print "Article from source: ", a.source, "feed: ", a.feed, " was invalid"

def isValid(a):
	if a.title == '':
		return False
	if a.url == '':
		return False
	if a.timestamp < 500:
		return False
	if a.source == '':
		return False
	if a.feed == '':
		return False
	if a.content == '':
		return False
	return True