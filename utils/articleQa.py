from difflib import SequenceMatcher
import db, datetime
#Quality control for single articles

def _similar(str1, str2):
    ratio = len(str1) / float(len(str2))
    if ratio < 0.9 or ratio > 1.1:
        return 0
    return SequenceMatcher(None, str1, str2).ratio()

def isDuplicate(article):
    threeDays = datetime.datetime.now() - datetime.timedelta(days=3)
    otherArticles = db.getLatestArticles({'source': article.source, 'timestamp': {'$gte': threeDays}})
    for otherArticleData in otherArticles:
        if article.title == otherArticle['title'].encode('utf-8') or _similar(article.content, otherArticle['content'].encode('utf-8')) > 0.9:
            return otherArticle['_id']
    return None
