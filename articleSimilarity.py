from difflib import SequenceMatcher
from dbco import *
import time

def largestTopics(days, limit):
    limit = int(limit); days = int(days)
    startTime = time.time() - days * 24 * 3600
    endTime = time.time()
    match = {"$match" : {"timestamp" : {"$gt" : startTime, "$lt" : endTime}, 'topic': {'$exists': True}}}
    group = {"$group" : {"_id" : "$topic", "count" : {"$sum" : 1}}}
    sort = {"$sort" : {"count" : -1}}
    limit = {"$limit" : limit}
    topicCounts = list(db.qdoc.aggregate([match, group, sort, limit]))

    return topicCounts

def similar(a, b):
	rat = len(a)/float(len(b))
	if rat < 0.9 or rat > 1.1:
		return 0
	return SequenceMatcher(None, a, b).ratio()

topic = list(largestTopics(2,2))[0]['_id']

today = time.time()
yesterday = today-86400

arts = list(db.qdoc.find({'topic': topic}))
print len(arts)


for i in range(0, len(arts)):
	for j in  range(i+1, len(arts)):
		a = arts[i]; b = arts[j]
		s = similar(a['content'], b['content'])
		if s > 0.3:
			print "-------------------------------------------"
			print s
			print a['source'], " vs. ", b['source']
			print a['timestamp']-b['timestamp']
			print a['title'].encode('utf-8')
			print b['title'].encode('utf-8')
			print a['url']
			print b['url']