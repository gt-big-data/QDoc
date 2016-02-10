from bson.objectid import ObjectId
import random

from dbco import db
from article import Article

# For backwards compatibility.
# Also for queries that don't fit any of the standard functions.
qdoc = db.qdoc

def _returnOrYieldArticles(query, shouldYield):
    if shouldYield:
        for article in query:
            yield Article(article)
    else:
        articles = []
        for article in query:
            articles.append(Article(article))
        return articles

def _returnOrYieldGeneral(query, shouldYield):
    if shouldYield:
        for general in query:
            yield general
    else:
        objects = []
        for general in query:
            objects.append(general)
        return objects

def getLatestArticles(findQuery=None, limit=None, shouldYield=False):
    findQuery = findQuery or {}
    query = db.qdoc.find(findQuery).sort('timestamp', -1)
    if limit is not None:
        query = query.limit(limit)
    return _returnOrYieldArticles(query, shouldYield)

def getFieldsOfLatestArticles(findQuery, fields, limit, shouldYield=False):
    findQuery = findQuery or {}
    query = db.qdoc.find(findQuery, fields).sort('timestamp', -1)
    if limit is not None:
        query = query.limit(limit)
    return _returnOrYieldGeneral(query, shouldYield)

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

def updateArticle(id, updatedValues):
    db.qdoc.update({'_id': ObjectId(id)}, {'$set': updatedValues})

def insertArticle(guid, values):
    db.qdoc.update({'guid': guid}, {'$set': values}, upsert=True)

def aggregateArticles(operations, shouldYield=False):
    query = db.qdoc.aggregate(operations)
    return _returnOrYieldArticles(query, shouldYield)

def aggregateFeeds(operations, shouldYield=False):
    query = db.feed.aggregate(operations)
    return _returnOrYieldGeneral(general, shouldYield)

def log(data):
    db.qdoc_log.insert_one(data)
