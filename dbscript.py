from sys import argv

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

commands = {
    'groupbadsources': checkBadSources
}

if __name__ == '__main__':
    if len(argv) < 2:
        printHelp()
    else:
        main(argv[1], argv[2:])
