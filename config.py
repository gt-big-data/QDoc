import os
env = os.environ.get('QDOC_ENV') or 'dev'
# if you are a server, set QDOC_ENV to 'prod' :)

variables = {
    'db_connection': {
        'prod': 'mongodb://db.retinanews.net:27017/',
        'dev': 'mongodb://localhost:27017/'
    },
    'feedsNum': {
        'prod': 150,
        'dev': 1
    },
    'batchSize': {
        'prod': 50,
        'dev': 1
    },
    'downloadFeedThreads': {
        'prod': 100,
        'dev': 1
    },
    'downloadArticleWorkers': {
        'prod': 4,
        'dev': 1
    },
    'parseWorkers': {
        'prod': 4,
        'dev': 1
    }
}

config = {}

for key in variables:
    config[key] = variables[key][env]
