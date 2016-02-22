from bson.objectid import ObjectId
import random

from dbco import db

# Expose actual collection names and better names that can be used inside of Python code.
qdoc = articles = db.qdoc # Crawled articles.
feed = feeds = db.feed # RSS feeds that may or not be in use right now.
test_sources = newFeeds = db.test_sources # RSS feeds that we think exist but haven't tried to use yet.
source_cleaning = source_cleaning = db.source_cleaning # Specific tags to remove for certain sources.

def _returnOrYield(query, shouldYield):
    if shouldYield:
        def generator():
            for obj in query:
                yield obj
        return generator
    else:
        objects = []
        for obj in query:
            objects.append(obj)
        return objects

def getLatestArticles(findQuery=None, limit=None, shouldYield=False):
    findQuery = findQuery or {}
    query = db.qdoc.find(findQuery).sort('timestamp', -1)
    query = query.limit(limit or 0)

    return _returnOrYield(query, shouldYield)

def getFieldsOfLatestArticles(findQuery, fields, limit, shouldYield=False):
    findQuery = findQuery or {}
    query = db.qdoc.find(findQuery, fields).sort('timestamp', -1)
    query = query.limit(limit or 0)

    return _returnOrYield(query, shouldYield)

def countArticles(findQuery=None):
    findQuery = findQuery or {}
    return db.qdoc.find(findQuery).count()

def getArticle(findQuery=None):
    findQuery = findQuery or {}
    query = db.qdoc.find(findQuery).limit(1)
    # Return the single article if it exists.
    for article in query:
        return toArticle(article)
    return None

def getArticleById(idString):
    return getArticle({'_id': ObjectId(idString)})

def getRandomRecentArticle():
    skipAmount = random.randint(0, 10000)
    query = db.qdoc.find({}).skip(skipAmount).limit(1)
    for article in query:
        return toArticle(article)
    return None

def updateArticle(id, newArticle): # this is an article object now
    db.qdoc.update({'_id': ObjectId(id)}, {'$set': {'content': newArticle.content, 'keywords': []}})

def insertArticle(guid, values):
    try:
        values = values.__dict__
    except AttributeError:
        pass
    db.qdoc.update({'guid': guid}, {'$set': values}, upsert=True)

def aggregateArticles(operations, shouldYield=False):
    query = db.qdoc.aggregate(operations)
    return _returnOrYield(query, shouldYield)

def aggregateFeeds(operations, shouldYield=False):
    query = db.feed.aggregate(operations)
    return _returnOrYield(query, shouldYield)

def bulkUpdateArticles(callback):
    bulkUpdate = db.qdoc.initialize_unordered_bulk_op()
    def updater(condition, updatedValues):
        bulkUpdate.find(condtion).upsert().update(updatedValues)
    callback(updater)
    bulkUpdate.execute()

def log(data):
    db.qdoc_log.insert_one(data)
