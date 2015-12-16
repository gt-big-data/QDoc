from difflib import SequenceMatcher
import sys, random, time
from article import *
from dbco import *

def similar(a, b):
	rat = len(a)/float(len(b))
	if rat < 0.9 or rat > 1.1:
		return 0
	return SequenceMatcher(None, a, b).ratio()

def isDuplicate(content, source):
	last = db.qdoc.find({'source': source, 'timestamp': {'$gte': (time.time()-3*86400)}}) # last 3 days
	for a in last:
		sim = similar(content, a['content'])
		if sim > 0.9:
			return a['_id']
	return None

if __name__ == '__main__':
	art = None
	if len(sys.argv) > 1:
		arti = list(db.qdoc.find({'_id': sys.argv[1]}).limit(1))
		if len(arti) > 0:
			art = arti[0]
	if art is None: # ow, get a random article
		art = list(db.qdoc.find({}).sort('timestamp', -1).skip(int(random.random()*1000)).limit(1))[0]

	content = "Oil at the first phase of separation from the sand at the Suncor tar sands processing plant near at their mining operations near Fort McMurray, Alberta, September 17, 2014. PARIS Canada's newly elected government is committed to being a strong ally in global efforts to curb climate change, but it is unclear yet what that will mean for its vast oil patch, Environment and Climate Change Minister Catherine McKenna said on Wednesday.\"We are committed to moving to a low-carbon economy and we need to look at what that means,\" McKenna said at a briefing on the sidelines of the U.N. climate conference in Paris.Canada's oil sands are among the largest petroleum reserves in the world, but efforts to expand their production have been stymied by a lack of pipeline capacity, heavy environmental opposition, and a recent slump in oil prices. [O/R]The industry suffered a setback last month when U.S. President Barack Obama rejected TransCanada's proposed Keystone XL oil sands pipeline into the United States citing environmental concerns.TransCanada has also proposed a bigger, all-Canadian pipeline east to the Atlantic province of New Brunswick, called Energy East, which would link some 1.1 million barrels per day of western Canadian oil to global markets by 2020.McKenna said that project was being reviewed.\"But I don't like just looking at one particular development. We are looking at how we are going to make progress toward a low-carbon economy. We are going to be looking at a whole range of solutions so that we ... have an ambitious, pan-Canadian plan to do our part,\" she said.She said that plan would be drawn up with input from provincial, territorial and indigenous leaders.The province of Alberta, home to the oil sands industry, recently announced plans to tax and limit carbon dioxide emissions, in a way that still gives more efficient oil-producing companies room to grow. Other provinces have also put forward carbon dioxide emissions reduction plans.Recently elected Liberal Prime Minister Justin Trudeau has sought to break with his long-serving predecessor, Conservative Stephen Harper, by embracing the fight against climate change."
	source = 'reuters'
	dupID = isDuplicate(content, source)

	print "This content is a duplicate of", dupID 