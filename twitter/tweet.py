from nltk.corpus import stopwords
from collections import namedtuple
import json, re
from dbco import *

stopW = set(stopwords.words('english'))
commW = ['http', 'like', 'ga', 'job', 'love', 'atlanta', 'amp', 'hiring', 'day', 'lol', 'know', 'time', 'want', 'got', 'good', 'shit', 'need', 'people', 'thank', 'today', 'really', 'make', 'careerarc', 'work', 'happy', 'great', 'going', 'nigga', 'think', 'come', 'new', 'life', 'school', 'right', 'll', 'feel', 'look', 'girl', 'night', 'thing', 'man', 'say', 've', 'friend', 'let', 'fuck', 'year', 'best', 'alway', 'way', 'wanna', 'tonight', 'game', 'better', 'birthday', 'mi', 'hate', 'latest', 'ain', 'im', 'tomorrow', 'u', 'gonna', 'home', 'god', 'getting', 'week', 'real', 'guy', 'oh', 'bad', 'sleep', 'morning', 'hope', 'tell', 'gotta', 'opening', 'bitch', 'said', 'click', 'baby', 'wait', 'ready', 'yall', 'boy', 'stop', 'didn', 'lmao', 'ya', 'start', 'damn', 'cause', 'talk', 'retail', 'team', 'follow', 'little', 'clas', 'mean', 'play']
commW.extend(stopW)
common_words = set(commW)

Tweet = namedtuple('Tweet', ['guid', 'text', 'author', 'timestamp', 'place', 'words', 'hashtags', 'mentions'])
class Tweet(namedtuple('Tweet', ['guid', 'text', 'author', 'timestamp', 'place', 'words', 'hashtags', 'mentions'])):
    def __new__(cls, guid='', text='', author='', timestamp=0, place='', words=[], hashtags=[], mentions=[]):
        return super(Tweet, cls).__new__(cls, guid, text, author, timestamp, place, words, hashtags, mentions)

def saveNewTweet(T):
	if isValid(T):
		insertTweet(T)

def remove_non_ascii_1(text):
	return ''.join(i for i in text if ord(i)<128)

def cleanTweet(tweet):
	global common_words
	tweetString = re.sub('[()!\.,\?&;]', '', tweet).lower()
	tweetString = remove_non_ascii_1(tweetString)
	tweetString = tweetString.replace('\n', '')
	words = tweetString.split(' ')
	words = [w for w in words if ('http' not in w and len(w) > 1 and not w.isdigit())]
	words = list(set(words)-common_words)
	hashtags = [w for w in words if w.startswith('#')]
	mentions = [w for w in words if w.startswith('@')]
	words = list((set(words)-set(hashtags))-set(mentions))
	return words, hashtags, mentions

def insertTweet(T):
	db.tweet.update({'guid': t['guid']}, {'$set': t}, upsert=True)

def isValid(t):
	# Verifies that a tweet has the minimal information needed
	if t.guid == '':
		return False
	if t.text == '':
		return False
	if t.author == '':
		return False
	if t.timestamp < 500:
		return False
	myText = t.text
	if len(t.words + t.hashtags + t.mentions) < 3:
		return False
	return True