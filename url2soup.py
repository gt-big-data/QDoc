from bs4 import BeautifulSoup, Comment, Doctype, NavigableString
import eventlet

global requests
requests = eventlet.import_patched('requests.__init__')

def url2soup(url):
	global requests
	try:
		html = requests.get(url, allow_redirects=True).text
	except:
		print url, "returned a 404 or some error"
		return BeautifulSoup('', 'html.parser')
	html = html.replace('<br>', '<br />')
	return BeautifulSoup(html, 'html.parser')