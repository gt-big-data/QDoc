import os
env = os.environ.get('QDOC_ENV') or 'dev'
# if you are a server, set QDOC_ENV to 'prod' :)

variables = {
    'db_connection': {
        'prod': 'mongodb://%s:27017/' % os.environ.get('QDOC_MONGO_HOST'),
        'dev': 'mongodb://%s:27017/' % 'localhost'
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
