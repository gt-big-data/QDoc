from pymongo import MongoClient, errors

#Production code: 'mongodb://146.148.59.202:27017/'
client = MongoClient('mongodb://146.148.59.202:27017/')
db = client['big_data']