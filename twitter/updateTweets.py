from dbco import *
from tweet import *

Ts = list(db.tweet.find({'words': {'$exists': False}}).limit(1000))

i = 1
for T in Ts:
	words, hashtags, mentions = cleanTweet(T['text'])
	T2 = Tweet(T['guid'], T['text'], T['author'], T['timestamp'], T['place'], words, hashtags, mentions)
	if isValid(T2):
		db.tweet.update({'guid': T['guid']}, {'$set': T2})
	else:
		i += 1
		print "Deleted ", i
		db.tweet.remove({'guid': T['guid']})

print db.tweet.find().count()