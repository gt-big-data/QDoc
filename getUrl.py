from bs4 import BeautifulSoup, Comment, Doctype, NavigableString
import concurrent.futures as futures # for multithreading
import sys, eventlet, time, warnings, requests
from dbco import *

warnings.filterwarnings("ignore")

def getUrl(url):
	time1 = time.time()
	try:
		req = requests.get(url, allow_redirects=True, verify=False,timeout=10)
	except Exception as e:
		status_code = str(e)
		return {'soup': BeautifulSoup('', 'html.parser'), 'finalURL': '', 'error': status_code} # some error happened

	html = (req.text).replace('<br>', '<br />')
	return {'soup': BeautifulSoup(html, 'html.parser'), 'finalURL': req.url}

def getURLs(urls):
	with futures.ThreadPoolExecutor(max_workers=100) as executor:
		return executor.map(getUrl, urls)

def getURLsEventlet(urls): # this is legacy now, it is slower...
	pool = eventlet.GreenPool()
	return [ret for ret in pool.imap(getUrl, urls)]

if __name__ == '__main__':
	urls = [a['url'] for a in list(db.qdoc.find({}, {'url': True}).limit(1200))]
	time2 = time.time()
	bla= getURLs(urls)
	print "MULTITHREADING : ", (time.time()-time2) ,"s"
	time1 = time.time()
	bla= getURLsEventlet(urls)
	print "EVENTLET METHOD: ", (time.time()-time1) ,"s"