from bs4 import BeautifulSoup
import concurrent.futures as futures # for multithreading
import warnings, requests

warnings.filterwarnings("ignore")

def getUrl(url):
	try:
		req = requests.get(url, allow_redirects=True, verify=False,timeout=10)
	except Exception as e:
		status_code = str(e)
		return {'soup': BeautifulSoup('', 'html.parser'), 'finalURL': '', 'error': status_code} # some error happened

	# TODO: Why are we doing this replacement? I'd be surprised if BeautifulSoup can't handle both types of tags.
	html = (req.text).replace('<br>', '<br />')
	return {'soup': BeautifulSoup(html, 'html.parser'), 'finalURL': req.url}

def getURLs(urls):
	with futures.ThreadPoolExecutor(max_workers=100) as executor:
		downloaded_urls = executor.map(getUrl, urls)
		# Force all feeds to download before finishing to prevent weird issues with the
		# ThreadPool shutting down before all of the tasks finishing.
		downloaded_urls = [d for d in downloaded_urls]
	return downloaded_urls
