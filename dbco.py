from pymongo import MongoClient, errors

# TODO: Move this to a config file.
client = MongoClient('mongodb://127.0.0.1:27017/')
db = client['big_data']
