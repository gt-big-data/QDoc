from bs4 import BeautifulSoup, Comment, Doctype, NavigableString
import eventlet,sys

global requests
requests = eventlet.import_patched('requests.__init__')

def url2soup(url):
	global requests
	try:
		html = requests.get(url, allow_redirects=True, verify=False).text
	except:
		print url, "returned a 404 or some error"
		return BeautifulSoup('', 'html.parser')
	html = html.replace('<br>', '<br />')
	return BeautifulSoup(html, 'html.parser')

def finalURL(url):
	return requests.get(url, allow_redirects=True, verify=False).url

if __name__ == '__main__':
	print finalURL(sys.argv[1])