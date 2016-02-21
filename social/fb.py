from bs4 import *
import requests

def url_counts(urls):
	ret = {}
	unitLength = 10
	while len(urls) > 0:
		currentUrl = urls
		if len(urls) > unitLength:
			currentUrl = urls[:unitLength]
			urls = urls[unitLength:]
		else:
			urls = []

		fbUrl = 'http://api.facebook.com/restserver.php?method=links.getStats&urls='+",".join(currentUrl)
		doc = BeautifulSoup(requests.get(fbUrl).text, 'html.parser')
		for d in doc.findAll('link_stat'):
			u = d.find('url').get_text()
			fb = d.find('total_count').get_text()
			ret[u] = fb
	return ret