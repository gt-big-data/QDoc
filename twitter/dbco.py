from pymongo import MongoClient, errors

client = MongoClient('localhost') # Old GCE instance: mongodb://146.148.59.202:27017/
db = client['big_data']