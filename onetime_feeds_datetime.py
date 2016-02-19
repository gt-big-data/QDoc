"""Run this script to convert all existing feeds to use datetime objects instead of seconds since 1970."""

import db
from datetime import datetime


def fixArticleIntStamps():
    bulkUpdate = db.qdoc.initialize_unordered_bulk_op()
    query = db.qdoc.find({'$or': [
        {'timestamp': {'$type': 'int'}},
        {'timestamp': {'$type': 'double'}},
    ]})
    shouldExecute = False
    for article in query:
        shouldExecute = True
        stamp = article.get('timestamp', 0)
        date = datetime.utcfromtimestamp(stamp)
        bulkUpdate.find({'timestamp': stamp}).update({'$set': {'timestamp': date}})

    if shouldExecute:
        bulkUpdate.execute()

def fixIntStamps():
    bulkUpdate = db.feed.initialize_unordered_bulk_op()
    query = db.feed.find({'$or': [
        {'stamp': {'$type': 'int'}},
        {'stamp': {'$type': 'double'}},
    ]})
    shouldExecute = False
    for feed in query:
        shouldExecute = True
        stamp = feed.get('stamp', 0)
        date = datetime.utcfromtimestamp(stamp)
        bulkUpdate.find({'stamp': stamp}).update({'$set': {'stamp': date}})

    if shouldExecute:
        bulkUpdate.execute()

def fixIntLastCrawl():
    bulkUpdate = db.feed.initialize_unordered_bulk_op()
    query = db.feed.find({'$or': [
        {'lastCrawl': {'$type': 'int'}},
        {'lastCrawl': {'$type': 'double'}},
    ]})
    shouldExecute = False
    for feed in query:
        shouldExecute = True
        crawl = feed.get('lastCrawl', 0)
        date = datetime.utcfromtimestamp(crawl)
        bulkUpdate.find({'lastCrawl': crawl}).update({'$set': {'lastCrawl': date}})

    if shouldExecute:
        bulkUpdate.execute()

print 'Fixing feed timestamps.'
fixIntStamps()
print 'Fixing feed lastcrawl timestamps.'
fixIntLastCrawl()
print 'Fixing article timestamps.'
fixArticleIntStamps()
