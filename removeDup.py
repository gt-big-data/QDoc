from difflib import SequenceMatcher
from dbco import *
import time

def similar(a, b):	
	if len(a) == 0 or len(b) == 0:
		return 0
	rat = len(a)/float(len(b))
	if rat < 0.9 or rat > 1.1:
		return 0
	return SequenceMatcher(None, a, b).ratio()

leastTime = time.time()-30*86400
match = {'$match': {'timestamp': {'$gte': leastTime}, 'topic': {'$exists': True}}}
group = {'$group': {'_id': '$topic', 'count': {'$sum': 1}}}
sort = {'$sort': {'count': -1}}
limit = {'$limit': 20}

pipeline = [match, group, sort,limit]
mostTopics = [t['_id'] for t in list(db.qdoc.aggregate(pipeline))]

mostTopics.pop(0);
mostTopics.pop(0);

for topic in mostTopics:
	arts = list(db.qdoc.find({'topic': topic}).sort('timestamp', -1))
	print float(len(arts)*(len(arts)-1))/2.0
	for i in range(len(arts)):
		for j in range(i+1, len(arts)):
			index = i*len(arts) + j
			if index%1000 == 999:
				print index
			if arts[i]['source'] == arts[j]['source'] and similar(arts[i]['content'], arts[j]['content']) > 0.98:
				print arts[i]['title']
				print arts[j]['title']
				toDelete = arts[i]['_id']
				if arts[j]['timestamp'] < arts[i]['timestamp']:
					toDelete = arts[j]['_id']

				db.qdoc.delete_one({'_id': toDelete})
				print similar(arts[i]['content'], arts[j]['content'])
				print "----------------------"
	print "DONE WITH TOPIC\n---------------------------------------------"