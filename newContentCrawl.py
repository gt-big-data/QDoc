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
def removeScriptStyle(soup):
    hnfs = soup.findAll({'style', 'script', 'noscript', '[document]', 'head', 'title', 'form'})
    [hnf.extract() for hnf in hnfs]
    return soup
def selectBadContent(item):
	classes = " ".join(item.get('class', [])).lower()
	if ' ad ' in classes or 'metadata' in classes or 'byline' in classes or 'location' in classes or 'modification' in classes or ' footer' in classes:
	# or 'caption' in classes, not possible due to aljazeera
		return True
	return False

def getText(soup):
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
				elem.already = True
		else:
			pass
	returnString = ''
	for st in buildText:
		returnString += re.sub(' +', ' ', st).replace('\t', '')
		if st[-1] in ['.', '!', '?']:
			returnString += '\n'
	return returnString.replace("’", "'").replace("”", '"').replace("“", '"').replace('—', '-').replace('‘', "'")

def getContent(soup):
	newContent = []
	# Cleanning phase
	removeComments(soup)
	removeScriptStyle(soup)
	removeHeaderNavFooter(soup)
	bads = [el.extract() for el in soup.findAll(selectBadContent)] # remove all bad content
	f = open("content.html", 'w'); f.write(soup.prettify().encode('utf-8')); f.close();

	# Finding content in the tree
	for el in soup.findAll(True):
		score = 0.0
		if el.name in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7'] and el.parent.name == '[document]':
			score += 3
		for c in el:
			if c.name == 'br': # business insider style
				score += 0.5
			if c.name in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7']:
				score += 1.0
		if score >= 3.0:
			newContent.append(getText(el))
	return '\n'.join(newContent).encode('utf-8').replace("’", "'").replace("”", '"').replace("“", '"').replace('—', '-').replace('‘', "'")


if __name__ == '__main__':
	source = 'cnn'; skip =  0
	find = {'source': 'aljazeera'}
	if len(sys.argv) > 1:
		find = {'_id': ObjectId(sys.argv[1])}
	if len(sys.argv) > 2:
		skip = int(sys.argv[2])

	rand = int(2000*random.random())
	any = False
	match = {'$match': {}}
	project = {'$project': {'_id': True, 'guid': True, 'title': True, 'url': True, 'feed': True, 'source': True, 'content': True, 'tsmod': {'$mod': ['$timestamp', rand]}}}
	sort = {'$sort': {'tsmod': -1}}
	limit = {'$limit': 30}
	articles = list(db.qdoc.aggregate([match, project, sort, limit]))
	
	for art in articles:
		html = urllib2.urlopen(art['url']).read().replace('<br>', '<br />')

		newContent = getContent(BeautifulSoup(html, 'html.parser'))
		article = Article(guid=art['guid'], title=art['title'], url=art['url'], timestamp=0, source=art['source'], feed=art['feed'])
		soup = htmlToSoup(article, html)
		parse(article, html)
		oldContent = article.content.encode('utf-8')
		simi = ratio(newContent, oldContent)
		if simi < 10.9:
			f = open("newContent.txt", 'w'); f.write(newContent); f.close();
			f = open("oldContent.txt", 'w'); f.write(oldContent); f.close();
			print art['source'], " | ", art['_id'], " | Sim: ", simi
			print "-----------------------------------------------------"