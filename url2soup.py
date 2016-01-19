from bs4 import BeautifulSoup, Comment, Doctype, NavigableString
import urllib2

class MyHTTPRedirectHandler(urllib2.HTTPRedirectHandler): # This handles redirects on the url :)
	def http_error_302(self, req, fp, code, msg, headers):
		return urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)
	http_error_301 = http_error_303 = http_error_307 = http_error_302

def url2soup(url):
	cookieprocessor = urllib2.HTTPCookieProcessor()
	urllib2.install_opener(urllib2.build_opener(MyHTTPRedirectHandler, cookieprocessor)) # to handle redirects
	try:
		html = urllib2.urlopen(url).read()
	except:
		print url, "returned a 404 or some error"
		return BeautifulSoup('', 'html.parser')
	html = html.replace('<br>', '<br />')
	return BeautifulSoup(html, 'html.parser')