import urllib2, re
from dateutil.parser import *
from PIL import ImageFile
from bs4 import BeautifulSoup, Comment, Doctype, NavigableString
import re

def htmlToSoup(article, html):
    soup = BeautifulSoup(html, 'html.parser')
    # This screws up business insider
    # art = soup.find('article')
    # if art is not None:
        # soup = art

    soup = removeHeaderNavFooter(soup)
    soup = removeComments(soup)
    soup = removeScriptStyle(soup)
    soup = removeAds(soup, article.source)
    return soup

def parse(article, html):
    soup = htmlToSoup(article, html)
    article.content = getContent(soup, article.source)
    article.img = getBiggestImg(article, soup)

def crawlContent(articles):
    """Download and crawl the URLs stored in several articles."""
    for article in articles:
        if article.url == '':
            continue
        try:
            html = urllib2.urlopen(article.url).read()
        except Exception:
            print("Could not download the article at %s." % article.url)
            continue
        parse(article, html)
    return articles

def getBiggestImg(a, soup):
    """Get the URL of the largest image on page."""
    bestUrl = ''
    maxDim = 0
    imgs = soup.findAll('img')
    for img in imgs:
        url = ''
        if img.has_attr('data-src-small'): # fucking CNN, can't get it right
            url = img.get('data-src-small')
        elif img.has_attr('src'):
            url = img.get('src')
        if url != '':
            if 'http://' not in url and a.source == 'business_insider':
                url = 'http://www.businessinsider.in'+url
            if 'doubleclick.net' not in url:
                sizes = getImageSizes(url)
                if sizes[1] is not None and (sizes[1][0]*sizes[1][1]) > maxDim:
                    maxDim = (sizes[1][0]*sizes[1][1])
                    bestUrl = url
    return bestUrl

def removeHeaderNavFooter(soup):
    hnfs = soup.findAll({'header', 'nav', 'footer', 'aside', 'figure'})
    [hnf.extract() for hnf in hnfs]
    return soup
def removeScriptStyle(soup):
    hnfs = soup.findAll({'style', 'script', 'noscript', '[document]', 'head', 'title', 'form'})
    [hnf.extract() for hnf in hnfs]
    return soup

def removeComments(soup):
    comments = soup.findAll(text=lambda text:isinstance(text, Comment))
    [comment.extract() for comment in comments]
    return soup
def removeAds(soup, source):
    ads = soup.findAll(adSelect(source))
    [ad.extract() for ad in ads]
    return soup

def adSelect(source): # this is the selector for ads, recommended articles, etc
    idList = ['most-popular-parsely', 'specialFeature', # Reuters
    'orb-footer', 'core-navigation', 'services-bar', 'bbc-news-services', # BBC
    'profile-cards', #VentureBeat
    'social-plugins_bottom', 'social-plugins', 'avcslide', # Business Insider
    'mobile-article-extra', # techcrunch
    ]
    classList = {}
    classList['cnn'] = ['pg-rail', 'ob_widget', 'zn-story-bottom', 'zn-body__footer', 'zn-staggered__col', 'el__video--standard', 'el__gallery--fullstandardwidth', 'el__gallery-showhide', 'el__gallery', 'el__gallery--standard', 'el__featured-video', 'zn-Rail', 'el__leafmedia', 'metadata', 'media__caption', 'el__embedded', 'ad--is-hidden', 'pg__branding', 'nav--plain-header']
    classList['reuters'] = ['reuters-share', 'article-header', 'shr-overlay', 'related-photo-credit', 'slider-module', 'column2', 'articleLocation']
    classList['business_insider'] = ['abusivetextareaDiv', 'LoginRegister', 'rhsb', 'TabsContList', 'rhs_nl', 'sticky', 'rhs', 'titleMoreLinks', 'ShareBox', 'Commentbox', 'commentsBlock', 'RecommendBlk', 'prvnxtbg', 'OUTBRAIN', 'AuthorBlock', 'seealso', 'Joindiscussion', 'subscribe_outer', 'ByLine', 'comment-class', 'bi_h2', 'margin-top', 'source', 'image-container']
    classList['venture_beat'] = ['vb_widget', 'entry-footer', 'navbar', 'site-header', 'mobile-post', 'widget-area', 'vb_image_source', 'wp-caption-text', 'boilerplate-label', 'post-boilerplate']
    classList['techcrunch'] = ['l-sidebar', 'article-extra', 'social-share', 'feature-island-container', 'announcement', 'header-ad', 'ad-top-mobile', 'ad-cluster-container', 'social-list', 'trending-title', 'trending-byline', 'nav', 'nav-col', 'nav-crunchbase', 'trending-head', 'menu-nav-modal']
    classList['bbc'] = ['site-brand', 'column--secondary', 'share', 'bbccom_slot', 'index-title', 'container-width-only', 'story-body__mini-info-list-and-share', 'off-screen', 'story-more']
    classList['guardian'] = ['content-footer', 'site-message', 'content__meta-container', 'submeta', 'l-header', 'block-share', 'share-modal__content']
    classList['aljazeera'] = ['unsupported-browser', 'component-articleOpinion', 'hidden-phone', 'relatedResources', 'articleOpinion-secondary', 'articleOpinion-comments', 'dynamicStoryHighlightList', 'brightcovevideo']
    classList['france24'] = ['col-2', 'on-air-board-outer', 'short-cuts-outer', 'location', 'modification']
    def filter(tag):
        if tag.has_attr('id') and tag.get('id') in idList:
            return True
        if tag.has_attr('class'):
            c = tag.get('class')
            for className in classList[source]:
                if className in c:
                    return True
        if source == 'reuters' and tag.name == 'p':
            tt = tag.get_text().lower()
            if 'reporting by' in tt or 'writing by' in tt or 'editing by' in tt:
                return True
        return False

    return filter

def getContent(soup, source):
    elems = soup.findAll(text=True and visible)
    buildText = []
    for elem in elems:
        if isinstance(elem, NavigableString):
            txt = elem
            if elem.parent.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'] and txt[-1] not in ['.', '!', '?']:
                txt += '.'
            score = calcScore(elem, txt)
            if score > 0:
                buildText.append(txt)
        else:
            pass
    returnString = ''
    for st in buildText:
        returnString += re.sub(' +', ' ', st).replace('\t', '')
        if st[-1] in ['.', '!', '?']:
            returnString += '\n'
    return returnString

def isDate(txt):
    try:
        dt = parse(txt)
        return True
    except:
        return False

def calcScore(el, txt):
    txtLower = txt.lower()
    score = 1 # you have to at least get to 0
    if len(txt) < 5:
        score -= 100
    if len(txt) > 100: # at least some sentence
        score += 50

    if isDate(txt):
        score -= 100
        return score
    if el.parent.name == 'a' and (txt[:6].lower() == 'read: ' or txt[:9].lower() == 'read more'):
        score -= 100
        return score
    if len(txt) <= 25:
        shareKeywords = ['facebook', 'twitter', 'google plus', 'email', 'linkedin', 'google+', 'whatsapp', 'pinterest', 'snapchat', 'share', 'report', 'skip', 'more', 'post', 'comment', 'tweet', 'print']
        for key in shareKeywords:
            if key in txtLower:
                score -= 30
    if len(txt) < 40 and ('join us on facebook' in txtLower or 'watch the full video here' in txtLower or 'image credit' in txtLower or 'image source' in txtLower or 'just watched' in txtLower or 'must watch' in txtLower):
        score -= 100
        return score
    if len(txt) <= 70:
        if ('created' in txtLower or 'date' in txtLower or 'photograph:' in txtLower or 'browser' in txtLower or 'adobe' in txtLower or 'try again' in txtLower or 'upgrade' in txtLower or 'please install' in txtLower):
            score -= 30
    if ('http://' in txt or '.com' in txt or '.org' in txt or 'www.' in txt) and ' ' not in txt: # what if it's a link
        score -= 30
    if txtLower in ['events', 'terms of service', 'home', 'privacy policy', 'venturebeat', 'mobile', 'guest', 'about', 'topics', 'more news', 'see also', 'close']:
        score -= 100
    return score

def visible(element):
    """Return true if the element is probably visible on page if you scrolled around."""
    if element.parent.name in ['style', 'script', 'noscript', '[document]', 'head', 'title']:
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
