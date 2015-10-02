from collections import namedtuple
import json
from dbco import * # this imports the db connexion

Tweet = namedtuple('Tweet', ['guid', 'text', 'author', 'timestamp', 'place'])
class Tweet(namedtuple('Tweet', ['guid', 'text', 'author', 'timestamp', 'place'])):
    def __new__(cls, guid='', text='', author='', timestamp=0, place=''):
        return super(Tweet, cls).__new__(cls, guid, text, author, timestamp, place)

def saveNewTweets(newTweets):
	Ts = []
	for t in newTweets:
		if isValid(t):
			Ts.append(t._asdict())
	if len(Ts) > 0:
		insertArticles(Ts)

def insertArticles(Ts):
	for t in Ts:
		db.tweet.update({'guid': t['guid']}, {'$set': t}, upsert=True) # if the GUID is already in the set

def isValid(t):
	if t.guid == '':
		return False
	if t.text == '':
		return False
	if t.author == '':
		return False
	if t.timestamp < 500:
		return False
	myText = t.text
	if len(myText) < 20 or len(myText.split(' ')) < 4:
		return False
	return True

# tw = Tweet('blala', 'hello my tweet', 'phili', 234567567)
# saveNewTweets([tw])