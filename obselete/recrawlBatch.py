from bson.objectid import ObjectId
from utils.articleParser import *
from dbco import *
import sys, socket, random, requests
import concurrent.futures as futures # for multithreading
socket.setdefaulttimeout(5)

def getUrl(url):
	try:
		req = requests.get(url, allow_redirects=True, verify=False,timeout=10)
	except Exception as e:
		status_code = str(e)
		return {'soup': BeautifulSoup('', 'html.parser'), 'finalURL': '', 'error': status_code} # some error happened

	html = (req.text).replace('<br>', '<br />')
	return {'soup': BeautifulSoup(html, 'html.parser'), 'finalURL': req.url}

def getURLs(urls):
	with futures.ThreadPoolExecutor(max_workers=100) as executor:
		downloaded_urls = executor.map(getUrl, urls)
		# Force all feeds to download before finishing to prevent weird issues with the
		# ThreadPool shutting down before all of the tasks finishing.
		downloaded_urls = [d for d in downloaded_urls]
	return downloaded_urls

def recrawlArt(art,urlReturn):
	urlReturn = getUrl(art['url'])
	if 'error' in urlReturn:
		print 'Error', urlReturn['error'], 'in article', art['_id']
		return None

	soup = urlReturn['soup']

	cleanHTML = soup.prettify().encode('utf8')

	oldContent = art.get('content', '').encode('utf8')
	newContent = getContent(soup, art['source']).encode('utf8')
	print art['_id'], " | Old: "+ str(len(oldContent)).center(5)+ " | New: "+str(len(newContent)).center(5)
	print art['url']
	return {'id': art['_id'], 'content': newContent}

def recrawlSource():
	left = db.qdoc.find({'recrawl': {'$exists': True}}).count()
	while left>0:
		any = False
		match = {'$match': {'recrawl': {'$exists': True}}}
		project = {'$project': {'_id': True, 'guid': True, 'title': True, 'url': True, 'feed': True, 'source': True, 'content': True}}
		limit = {'$limit': 30}

		articles = list(db.qdoc.aggregate([match, project, limit]))

		qdocUpdate = db.qdoc.initialize_unordered_bulk_op()

		results = getURLs([a['url'] for a in articles])
		for res, art in zip(results, articles):
			ret = recrawlArt(art,res)
			if ret['content']:
				any = True
				qdocUpdate.find({'_id': ret['id']}).upsert().update({'$set': {'content': ret['content']}, '$unset': {'recrawl': True}})

		if any:
			qdocUpdate.execute()
		left = db.qdoc.find({'recrawl': {'$exists': True}}).count()
		print "-------------------------------------"		
		print "Left: ", left

recrawlSource()