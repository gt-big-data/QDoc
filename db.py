from bson.objectid import ObjectId
import random

from dbco import db
from article import Article

def getLatestArticles(findQuery=None, limit=None):
    findQuery = findQuery or {}
    query = db.qdoc.find(findQuery).sort('timestamp', -1)
    if limit is not None:
        query = query.limit(limit)
    for article in query:
        yield Article(article)

def countArticles(findQuery=None):
    findQuery = findQuery or {}
    return db.qdoc.find(findQuery).count()

def getArticle(findQuery=None):
    findQuery = findQuery or {}
    query = db.qdoc.find(findQuery).limit(1)
    # Return the single article if it exists.
    for article in query:
        return Article(article)
    return None

def getArticleById(idString):
    return getArticle({'_id': ObjectId(idString)})

def getRandomRecentArticle():
    skipAmount = random.randint(0, 10000)
    query = db.qdoc.find({}).skip(skipAmount).limit(1)
    for article in query:
        return Article(article)
    return None
