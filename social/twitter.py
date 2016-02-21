from  twython import Twython
import json

global twitter
twitter = 0

def loadTwitter():
	global twitter
	with open('credentials.json') as f:
		credentials = json.load(f)
	twitter = Twython(credentials['APP_KEY'],credentials['APP_SECRET'],credentials['ACCESS_TOKEN'],credentials['ACCESS_TOKEN_SECRET'])

def twitterCount(query):
	global twitter
	if twitter == 0:
		loadTwitter()
	return len(twitter.search(q=query, count=100)['statuses'])

if __name__ == '__main__':
	from dbco import *
	urls = [a['url'] for a in db.qdoc.find().sort('timestamp',- 1).limit(100)]
	for url in urls:
		c = twitterCount(url)
		print url, " => ", c