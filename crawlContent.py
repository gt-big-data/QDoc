import urllib, urllib2
from PIL import ImageFile
from bs4 import BeautifulSoup, Comment, Doctype, NavigableString

def crawlContent(articles):
	for i in range(0, len(articles)):
		a = articles[i]
		if a.url != '':
			try:
				html = urllib2.urlopen(a.url).read()
				soup = BeautifulSoup(html, 'html.parser')
				soup = removeHeaderNavFooter(soup)
				soup = removeComments(soup)
				soup = removeAds(soup)

				cont = getContent(soup)
				a = a._replace(content=cont)

				bestImage = getBiggestImg(a, soup)
				a = a._replace(img=bestImage)

				articles[i] = a
				with open("test.html", "w") as f:
					f.write(soup.prettify('utf-8'))
				with open("test.txt", "w") as f:
					f.write(cont)
			except:
				pass;

	return articles

def getBiggestImg(a, soup):
	bestUrl = ''
	maxDim = 0
	imgs = soup.findAll('img')
	for img in imgs:
		if img.has_attr('src'):
			url = img.get('src')
			if 'http://' not in url and a.source == 'business_insider':
				url = 'http://www.businessinsider.in'+url
			if 'doubleclick.net' not in url:
				sizes = getImageSizes(url)
				if sizes[1] is not None and (sizes[1][0]*sizes[1][1]) > maxDim:
					maxDim = (sizes[1][0]*sizes[1][1])
					bestUrl = url
	return bestUrl

def removeHeaderNavFooter(soup):
	hnfs = soup.findAll({'header', 'nav', 'footer'})
	[hnf.extract() for hnf in hnfs]
	return soup

def removeComments(soup):
	comments = soup.findAll(text=lambda text:isinstance(text, Comment) or text.find('if') != -1)
	[comment.extract() for comment in comments]
	return soup
def removeAds(soup):
	ads = soup.findAll(adSelect)
	[ad.extract() for ad in ads]
	return soup

def adSelect(tag): # this is the selector for ads, recommended articles, etc
	idList = ['most-popular-parsely', 'specialFeature', # Reuters
	'orb-footer', 'core-navigation', 'services-bar' # BBC
	]
	classList = ['ob_widget', 'zn-staggered__col', # CNN
	'reuters-share', # reuters
	'seealso', 'navBar', 'titleMoreLinks', 'RecommendBlk', 'AuthorBlock', 'Joindiscussion', 'TrendingBlk', 'subscribe_block', 'rhs', 'rhs_nl', 'footer', 'commentsBlock', # BusinessInsider
	'vb_widget', 'entry-footer', 'navbar', 'site-header', # VentureBeat
	'l-sidebar', 'article-extra', #Techcrunch
	'site-brand', 'column--secondary', 'share' # BBC
	]
	if tag.has_attr('id') and tag.get('id') in idList:
		return True
	if tag.has_attr('class'):
		c = tag.get('class')
		for className in classList:
			if className in c:
				return True
	return False

def getContent(soup):
	elems = soup.findAll(text=True and visible)
	buildText = []
	for elem in elems:
		if isinstance(elem, NavigableString):
			txt = elem.encode('utf-8')
			score = calcScore(elem, txt)
			# print "[",score,"]", txt
			if score > 0:
				buildText.append(txt)
		else:
			pass
	return "\n".join(buildText)

def calcScore(el, txt):
	score = 1 # you have to at least get to 0
	if len(txt) < 5:
		score -= 100
	if len(txt) > 50: # at least some sentence
		score += 50
	if ('http://' in txt or '.com' in txt or '.org' in txt or 'www.' in txt) and ' ' not in txt: # what if it's a link
		score -= 30
	if txt in ['Events', 'Terms of Service', 'Home', 'Privacy Policy', 'VentureBeat', 'Mobile', 'Guest', 'About']:
		score -= 100
	return score

def visible(element):
	if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
		return False
	return True

def getImageSizes(uri):
	# get file size *and* image size (None if not known)
	# http://effbot.org/zone/pil-image-size.htm
	try:
		file = urllib2.urlopen(uri, timeout=0.5)
		size = file.headers.get("content-length")
		if size: size = int(size)
		p = ImageFile.Parser()
		while 1:
			data = file.read(1024)
			if not data:
				break
			p.feed(data)
			if p.image:
				return size, p.image.size
				break
		file.close()
		return size, None
	except:
		return [0, [0,0]]
