from bs4 import BeautifulSoup, Comment, Doctype, NavigableString, UnicodeDammit
import re, tld
import db

unicodePunctuation =  u'\u2013\u2014\u2015\u2017\u2018\u2019\u201a\u201b\u201c\u201d\u201e\u2032\u2033'
asciiPunctuation = u'-     -     -     _     \'    \'    ,     \'    \"    \"    \"    \'    \"'
asciiPunctuation = asciiPunctuation.replace(' ', '')
punctuationTranslation =  dict((ord(uchar), achar) for uchar, achar in zip(unicodePunctuation, asciiPunctuation))

def clean(s):
    s = unicode(s)
    s = s.translate(punctuationTranslation)
    s = s.replace(u'\xe2\x80\x99', "'") # Replace a weird smart quote.
    s = s.strip()
    return s

def parseArticle(article):
    print 'Parsing %s' % article.url
    if len(article.html) == 0:
        print 'Article has no HTML. Cannot parse.'
        return False

    article.source = tld.get_tld(article.url)

    soup = BeautifulSoup(article.html, 'html.parser')
    # TODO: Heavily refactor getContent(...) and everything it calls.
    article.content = getContent(soup, article.source)
    return True

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

def removeBadContent(soup):
    removeIds(soup, ['comments'])
    removeClasses(soup, ['bottom', 'footer', 'notes'])
    for el in soup.findAll(True):
        classes = u" ".join(el.get('class', [])).lower()
        badClasses = [' ad ', 'metadata', 'byline', 'dateline', 'published', 'location', 'modification', ' footer', 'discussion', 'carousel', 'short-cuts', 'nocontent']
        for cl in badClasses:
            if cl in classes:
                el.extract()
                break

# TODO: This always throws an exception and returns False because parse is not defined.
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
    if (el.parent.name == 'a' and (txt[:6].lower() == 'read: ' or txt[:9].lower() == 'read more')) or txt[:9] == '(FRANCE24' or txt[:10] == '(FRANCE 24':
        score -= 100
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

def removeClasses(soup, classes):
    classes = set(classes)
    [el.extract() for el in soup.findAll(True) if len(set(el.get('class', [])) & classes) > 0]
def removeIds(soup, ids):
    [el.extract() for el in soup.findAll(True) if el.get('id', '') in ids]

def genericCleaning(soup):
    removeComments(soup)
    removeScriptStyle(soup)
    removeHeaderNavFooter(soup)
    removeBadContent(soup)

def sourceSpecificcleaning(soup, source):
    sourceCleaning = list(db.source_cleaning.find({'source': source})) # Load the source specific data
    if len(sourceCleaning) > 0:
        sourceCleaning = sourceCleaning[0]
        removeClasses(soup, sourceCleaning.get('classList', []))
        removeIds(soup, sourceCleaning.get('idList', []))
        for text in sourceCleaning.get('textList', []):
            [elem.extract() for elem in soup(text=re.compile(r''+text))]

def getText(soup, putAlready=True):
    elems = soup.findAll(text=True and visible)
    buildText = []
    for elem in elems:
        if isinstance(elem, NavigableString) and not hasattr(elem, 'already'):
            txt = elem
            if elem.parent.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'] and txt[-1] not in ['.', '!', '?']:
                txt += '.'
            score = calcScore(elem, txt)
            if score > 0:
                if txt[-1] not in ['.', '!', '?'] and elem.parent.name in ['p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li'] and len(elem.find_next_siblings()) == 0:
                    txt += '\n' # we are at the end of a paragraph
                if elem.parent.name == 'p' and len(elem.find_previous_siblings()) == 0:
                    txt = '\n'+txt # we are at the beginning of a paragraph
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
    return returnString

def getContent(soup, source=''):
    newContent = []
    # Cleanning phase
    genericCleaning(soup)
    sourceSpecificcleaning(soup, source)

    # f = open("content.html", 'w'); f.write(soup.prettify().encode('utf-8')); f.close();

    # Finding content in the tree
    bestElem = None; bestText = '';
    for el in soup.findAll(True):
        score = 0.0;  hasTitle = False
        if el.name in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7'] and el.parent.name == '[document]':
            score += 3
        for c in el:
            if c.name == 'br': # business insider style
                score += 0.5
            if c.name == 'p':
                score += 1.0
            if not hasTitle and c.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7']:
                score += 1.0
                hasTitle = True
        if score >= 3.0: # at least 3 paragraphs
            textOutput = getText(el)
            if float(len(textOutput))/score > 20.0: # we need at least 20 characters per container
                newContent.append(textOutput)
        elif score >= 1.0:
            if bestElem is None:
                bestElem = el; bestText = getText(el, False)
            else:
                a = getText(el, False)
                if bestElem is None or len(a) > len(bestText):
                    bestElem = el; bestText = a
    if len(newContent) == 0 and bestElem is not None: # in case nothing had a score of 3, but something had a score of 1 or more
        newContent.append(bestText)

    finalText = UnicodeDammit(u'\n'.join(newContent), smart_quotes_to='ascii').unicode_markup
    return finalText.replace('\n\n', '\n')
