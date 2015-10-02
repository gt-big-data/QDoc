import pymongo
from article import Article
from crawlContent import crawlContent

m = pymongo.MongoClient("146.148.59.202", 27017)
db = m.big_data

iterator = db.qdoc.find({"keywords" : {"$in" : ["hours ago"]}})

for doc in iterator:
    # update keywords
    new_keywords = [i for i in doc['keywords'] if i != "hours ago"]
    db.qdoc.update({"_id" : doc['_id']}, {"$set" : {"keywords" : new_keywords}}, upsert=False)
    # update content
    art = [Article(doc['_id'], doc['title'], doc['url'], doc['timestamp'], doc['source'], doc['feed'])]
    art = crawlContent(art)
    new_content = art[0].content
    db.qdoc.update({"_id" : doc['_id']}, {"$set" : {"content" : new_content}}, upsert=False)