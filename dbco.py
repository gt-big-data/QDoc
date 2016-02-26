from pymongo import MongoClient, errors
from config import config

# Set to 'api.retinanews.net' in production.
# ^ Not sure if that is needed with our QDOC_MONGO_HOST env variable
# mongodb://146.148.59.202:27017/ old GCE

dbConnection = config['db_connection']
print('Connecting to Mongo at %s' % dbConnection)
client = MongoClient(dbConnection)
db = client['big_data']
