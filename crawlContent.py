import urllib, urllib2
from dateutil.parser import *
from PIL import ImageFile
from bs4 import BeautifulSoup, Comment, Doctype, NavigableString

# TODO: Remove need for strange global variable.
source = ''

# TODO: Split this up so an individual article can be crawled.
def crawlContent(articles):
    """Download and crawl the URLs stored in several articles."""
    global source
    for i in range(0, len(articles)):
        a = articles[i]
        if a.url != '':
            try:
                html = urllib2.urlopen(a.url).read()
                source = a.source
                soup = BeautifulSoup(html, 'html.parser')
                soup = removeHeaderNavFooter(soup)
                soup = removeComments(soup)
                soup = removeScriptStyle(soup)
                soup = removeAds(soup)

                cont = getContent(soup)

                a = a._replace(content=cont)

                bestImage = getBiggestImg(a, soup)
                a = a._replace(img=bestImage)

                articles[i] = a
                # with open("test.html", "w") as f:
                #     f.write(soup.prettify('utf-8'))

            except:
                pass;
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
    hnfs = soup.findAll({'header', 'nav', 'footer', 'aside'})
    [hnf.extract() for hnf in hnfs]
    return soup
def removeScriptStyle(soup):
    hnfs = soup.findAll({'style', 'script', 'noscript', '[document]', 'head', 'title', 'form'})
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
    'orb-footer', 'core-navigation', 'services-bar', # BBC
    'profile-cards' #VentureBeat
    ]
    classList = {}
    classList['cnn'] = ['ob_widget', 'zn-staggered__col', 'el__video--standard', 'el__gallery--fullstandardwidth', 'el__gallery-showhide', 'el__gallery', 'el__gallery--standard', 'el__featured-video', 'zn-Rail', 'el__leafmedia']
    classList['reuters'] = ['reuters-share']
    classList['business_insider'] = ['abusivetextareaDiv', 'LoginRegister', 'rhsb', 'TabsContList', 'rhs_nl', 'sticky', 'rhs', 'titleMoreLinks', 'ShareBox', 'Commentbox', 'commentsBlock', 'RecommendBlk', 'prvnxtbg', 'OUTBRAIN', 'AuthorBlock', 'seealso', 'Joindiscussion', 'subscribe_outer']
    classList['venture_beat'] = ['vb_widget', 'entry-footer', 'navbar', 'site-header', 'mobile-post', 'widget-area']
    classList['techcrunch'] = ['l-sidebar', 'article-extra', 'social-share', 'feature-island-container', 'announcement', 'header-ad', 'ad-top-mobile', 'ad-cluster-container', 'social-list', 'trending-title', 'trending-byline', 'nav', 'nav-col', 'nav-crunchbase', 'trending-head']
    classList['bbc'] = ['site-brand', 'column--secondary', 'share', 'bbccom_slot']
    classList['guardian'] = ['content-footer', 'site-message', 'content__meta-container', 'submeta', 'l-header', 'block-share', 'share-modal__content']
    classList['aljazeera'] = ['unsupported-browser', 'component-articleOpinion', 'hidden-phone', 'relatedResources', 'articleOpinion-secondary', 'articleOpinion-comments', 'dynamicStoryHighlightList', 'brightcovevideo']
    classList['france24'] = ['col-2', 'on-air-board-outer', 'short-cuts-outer']
    if tag.has_attr('id') and tag.get('id') in idList:
        return True
    if tag.has_attr('class'):
        c = tag.get('class')
        for className in classList[source]:
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
            if score > 0:
                # print "[",score,"]", txt
                buildText.append(txt)
        else:
            pass
    return "\n".join(buildText)

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
    if len(txt) <= 25:
        shareKeywords = ['facebook', 'twitter', 'google plus', 'email', 'linkedin', 'google+', 'whatsapp', 'pinterest', 'snapchat', 'share', 'report', 'skip', 'more', 'post', 'comment', 'tweet', 'print']
        for key in shareKeywords:
            if key in txtLower:
                score -= 30
    if len(txt) <= 70:
        if ('created' in txtLower or 'date' in txtLower or 'photograph:' in txtLower or 'browser' in txtLower or 'adobe' in txtLower or 'try again' in txtLower or 'upgrade' in txtLower or 'please install' in txtLower):
            score -= 30
    if ('http://' in txt or '.com' in txt or '.org' in txt or 'www.' in txt) and ' ' not in txt: # what if it's a link
        score -= 30
    if txt in ['Events', 'Terms of Service', 'Home', 'Privacy Policy', 'VentureBeat', 'Mobile', 'Guest', 'About', 'Topics', 'More news', 'See Also', 'close']:
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
