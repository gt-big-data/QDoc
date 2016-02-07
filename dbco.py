from pymongo import MongoClient, errors
import os
# Set to 'api.retinanews.net' in production.
host = os.environ['QDOC_MONGO_HOST'] or 'localhost'

client = MongoClient('mongodb://%s:27017/' % host) # mongodb://146.148.59.202:27017/ old GCE
db = client['big_data']
