from sys import argv
from pprint import pprint

import db

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

commands = {
    'groupbadsources': checkBadSources,
    'getbadsource': getBadSource
}

if __name__ == '__main__':
    if len(argv) < 2:
        printHelp()
    else:
        main(argv[1], argv[2:])
