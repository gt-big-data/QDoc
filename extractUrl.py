from bs4 import BeautifulSoup, Comment, Doctype, NavigableString
from newContentCrawl import *
import sys, urllib2

# Things that can be added:
#NY Times
# Wikinews: https://en.wikinews.org/w/index.php?title=Special:NewsFeed&feed=rss&categories=Published&notcategories=No%20publish%7CArchived%7cAutoArchived%7cdisputed&namespace=0&count=15&ordermethod=categoryadd&stablepages=only
# i24news: http://www.i24news.tv/en/news/international/98362-160108-report-uk-australia-helping-saudi-in-yemen-campaign

class MyHTTPRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        print "Cookie Manip Right Here"
        return urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)

    http_error_301 = http_error_303 = http_error_307 = http_error_302

cookieprocessor = urllib2.HTTPCookieProcessor()

opener = urllib2.build_opener(MyHTTPRedirectHandler, cookieprocessor)
urllib2.install_opener(opener)

if len(sys.argv) > 1:
	myUrl = sys.argv[1]
	req = urllib2.Request(myUrl, headers={'User-Agent' : "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; it-it) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16"})
	html = urllib2.urlopen(req).read().replace('<br>', '<br />')
	newContent = getContent(BeautifulSoup(html, 'html.parser'), 'nosource')
	print newContent

else:
	print "Provide a URL"