from difflib import SequenceMatcher
from dbco import *
import time
#Quality control for single articles

def _similar(str1, str2):
	ratio = len(str1) / float(len(str2))
	if ratio < 0.9 or ratio > 1.1:
		return 0
	return SequenceMatcher(None, str1, str2).ratio()

def isDuplicate(article):
	threeDays = time.time() - (3 * 86400)
	otherArticles = db.qdoc.find({'source': a.source, 'timestamp': {'$gte': threeDays}}).sort('timestamp', -1)
	for otherArticle in otherArticles:
		if article.title == otherArticles['title'] or _similar(article.content, unicode(otherArticle['content'])) > 0.9:
			return otherArticle['_id']
	return None
