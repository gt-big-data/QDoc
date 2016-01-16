# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup, Comment, Doctype, NavigableString
from bson.objectid import ObjectId
from dbco import *
from article import *
import sys, urllib2
from crawlContent import *
from Levenshtein import ratio

def removeComments(soup):
	[e.extract() for e in soup(text=lambda text: isinstance(text, Comment))]

def removeHeaderNavFooter(soup):
    hnfs = soup.findAll({'header', 'nav', 'footer', 'aside', 'figure', 'button'})
    [hnf.extract() for hnf in hnfs]
    return soup
def html2soup(html):
	html = html.replace('<br>', '<br />')
	return BeautifulSoup(html, 'html.parser')
def removeScriptStyle(soup):
    hnfs = soup.findAll({'style', 'script', 'noscript', '[document]', 'head', 'title', 'form'})
    [hnf.extract() for hnf in hnfs]
    return soup
def removeBadContent(soup):
	for el in soup.findAll(True):
		classes = " ".join(el.get('class', [])).lower()
		badClasses = [' ad ', 'metadata', 'byline', 'dateline', 'location', 'modification', ' footer', 'discussion', 'carousel', 'short-cuts']
		for cl in badClasses:
			if cl in classes:
				# print cl
				el.extract()
				break

def removeClasses(soup, classes):
	classes = set(classes)
	[el.extract() for el in soup.findAll(True) if len(set(el.get('class', [])) & classes) > 0]
def removeIds(soup, ids):
	for i in ids:
		[el.extract() for el in soup.find(id=i)]

def genericCleaning(soup):
	removeComments(soup)
	removeScriptStyle(soup)
	removeHeaderNavFooter(soup)
	removeBadContent(soup)

def sourceSpecificcleaning(soup, source):
	if source == 'reuters':
		removeClasses(soup, ['column2'])
	if source == 'cnn':
		removeClasses(soup, ['nav--plain-header', 'pg-rail--right', 'media__video'])
	if source == 'guardian':
		removeClasses(soup, ['submeta', 'content-footer'])
	if source == 'business_insider':
		removeClasses(soup, ['seealso', 'comment-class'])
		removeIds(soup, ['avcslide'])

def getText(soup, putAlready=True):
	reload(sys)
	sys.setdefaultencoding('utf8') # magic sauce
	elems = soup.findAll(text=True and visible)
	buildText = []
	for elem in elems:
		if isinstance(elem, NavigableString) and not hasattr(elem, 'already'):
			txt = elem
			if elem.parent.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'] and txt[-1] not in ['.', '!', '?']:
				txt += '.'
			score = calcScore(elem, txt)
			if score > 0:
				buildText.append(txt)
				if putAlready:
					elem.already = True
		else:
			pass
	returnString = ''
	for st in buildText:
		returnString += re.sub(' +', ' ', st).replace('\t', '')
		if st[-1] in ['.', '!', '?']:
			returnString += '\n'
	returnString = returnString.replace("’", "'").replace("”", '"').replace("“", '"').replace('—', '-').replace('‘', "'")
	return returnString

def getContent(soup, source=''):
	newContent = []
	# Cleanning phase
	genericCleaning(soup)
	sourceSpecificcleaning(soup, source)
	
	f = open("content.html", 'w'); f.write(soup.prettify().encode('utf-8')); f.close();

	# Finding content in the tree
	bestElem = None; bestText = ''
	for el in soup.findAll(True):
		score = 0.0
		if el.name in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7'] and el.parent.name == '[document]':
			score += 3
		for c in el:
			if c.name == 'br': # business insider style
				score += 0.5
			if c.name in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7']:
				score += 1.0
		if score >= 3.0: # at least 2 paragraphs
			dewtf = getText(el)
			newContent.append(dewtf)
		elif score >= 1.0:
			if bestElem is None:
				bestElem = el; bestText = getText(el, False)
			else:
				a = getText(el, False)
				if bestElem is None or len(a) > len(bestText):
					bestElem = el; bestText = a
	if len(newContent) == 0 and bestElem is not None: # in case nothing had a score of 3, but something had a score of 1 or more
		newContent.append(bestText)
	return '\n'.join(newContent).encode('utf-8').replace("’", "'").replace("”", '"').replace("“", '"').replace('—', '-').replace('‘', "'")

if __name__ == '__main__':
	while True:
		find = {}
		if len(sys.argv) > 1:
			find = {'_id': ObjectId(sys.argv[1])}

		rand = int(2000*random.random())
		match = {'$match': find}
		project = {'$project': {'_id': True, 'guid': True, 'title': True, 'url': True, 'feed': True, 'source': True, 'content': True, 'tsmod': {'$mod': ['$timestamp', rand]}}}
		sort = {'$sort': {'tsmod': -1}}
		limit = {'$limit': 30}
		articles = list(db.qdoc.aggregate([match, project, sort, limit]))
		
		for art in articles:
			try:
				html = urllib2.urlopen(art['url']).read()
			except:
				print "Error 404: Not Found"
				continue
			soup = html2soup(html)
			newContent = getContent(soup, art['source'])
			article = Article(guid=art['guid'], title=art['title'], url=art['url'], timestamp=0, source=art['source'], feed=art['feed'])
			soup = htmlToSoup(article, html)
			parse(article, html)
			oldContent = article.content.encode('utf-8')
			simi = ratio(newContent, oldContent)
			f = open("newContent.txt", 'w'); f.write(newContent); f.close();
			f = open("oldContent.txt", 'w'); f.write(oldContent); f.close();
			if simi < 0.8:
				print art['source'], " | ", art['_id'], " | Sim: ", simi
				print art['url']
				print "-----------------------------------------------------"
			else:
				sys.stdout.write("1")