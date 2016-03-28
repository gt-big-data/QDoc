from sys import argv
from pprint import pprint

import db
from feed import Feed
from article import Article

def printHelp(*args):
    print 'Usage: python %s <command> [args]' % argv[0]
    print
    print 'Commands:'
    for key, value in commands.items():
        print key
    print

def main(command, args):
    # Grab the appropriate function and execute it.
    commands.get(command, printHelp)(args)

def checkBadSources(args):
    match = {'$match': {'formatError': {'$exists': True}}}
    group = {'$group': {'_id': '$formatError', 'sum': {'$sum': 1}}}
    formatErrors = db.test_sources.aggregate([match, group])
    for error in formatErrors:
        print 'REASON: "%s"; COUNT: %d' % (error['_id'], error['sum'])

def getBadSource(args):
    if len(args) != 1:
        print 'No reason given. Run `python %s groupbadsources` for reasons.' % argv[0]
        return

    reason = args[0]
    badFeeds = db.test_sources.find({'formatError': reason}).limit(1)
    # badFeeds either has 0 or 1 feed in it.
    for onlyFeed in badFeeds:
        print 'Feed with error: %s' % reason
        pprint(onlyFeed, width=1)
        return
    print 'Could not find a feed with error: %s' % reason

def feedStatus(args):
    if len(args) != 1:
        print 'No feed given. Please specify a link to an RSS feed to view.'
        return
    feed = args[0]
    feeds = db.test_sources.find({'rss': feed}).limit(1)
    # feeds either has 0 or 1 feed in it.
    for onlyFeed in feeds:
        pprint(onlyFeed, width=1)
        return
    print 'We do not know about a feed at %s' % feed

def checkFeed(args):
    if len(args) != 1:
        print 'No feed given. Please specify a link to an RSS feed to re-classify.'
        return

    print 'Existing feed data:'
    feedStatus(args)

    feed = Feed(url=args[0])
    print 'Working with: %s' % feed.url

    print 'Attempting to download the feed.'
    couldDownload = feed.downloadFeed()
    if not couldDownload:
        print 'Could not download the feed. Is the URL correct? Is their site up? Is GTWifi working for you right now?'
        return
    print 'Successfully downloaded the feed.'

    print 'Attempting to parse the feed.'
    parseError, stats = feed.parseFeed()
    if parseError is None:
        print 'Successfully parsed the feed.'
        print stats

    if len(feed.articles) == 0:
        print 'No articles parsed. Something is wrong'

def parseArticle(args):
    if len(args) != 1:
        print 'No article given. Please specify a link to an article to parse.'
        return

    article = Article(url=args[0])
    print 'Working with: %s' % article.url

    print 'Attempting to download the article.'
    couldDownload = article.downloadArticle()
    if not couldDownload:
        print 'Could not download the article. Is the URL correct? Is their site up? Is GTWifi working for you right now?'
        return
    print 'Successfully downloaded the article.'
    article.parseArticle()
    print 'Article body:'
    print article.content

commands = {
    'groupbadsources': checkBadSources,
    'getbadsource': getBadSource,
    'feedstatus': feedStatus,
    'checkfeed': checkFeed,
    'parsearticle': parseArticle
}

if __name__ == '__main__':
    if len(argv) < 2:
        printHelp()
    else:
        main(argv[1], argv[2:])
