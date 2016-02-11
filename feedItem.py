"""This file deals with everything related to taking an individual item on a feed and turning it into an article."""
from dateutil import parser
import pytz

from article import Article

def feedItemToArticle(item):
    url = _extractLink(item)
    if url is None:
        print 'Could not find an article URL from the given feed item. Skipping.'
        return None

    title = _extractTitle(item)
    if title is None:
        print 'Could not find an article title from the given feed item. Skipping.'
        return None

    guid = _extractGuid(item)
    if guid is None:
        print 'Could not find a GUID for the given feed item. Skipping.'
        return None

    pubtime = _extractPubTime(item)
    if pubtime is None:
        print 'Could not find a pubtime for the given feed item. Skipping.'
        return None

    return Article(guid=guid, title=title, url=url, timestamp=pubtime)

def _extractPubTime(item):
    pubText = ''
    if item.pubdate is not None:
        pubText = item.pubdate.text
    elif item.published is not None:
        pubText = item.published.text
    if pubText == '':
        return None
    try:
        # TODO: Strongly consider removing dependency on dateutil and pytz.
        pubtime = parser.parse((re.sub("[\(\[].*?[\)\]]", "", pubText))).replace(tzinfo=pytz.utc)
        return pubtime # also remove anything between parentheses
    except:
        return None

def _extractGuid(item):
    if item.guid is not None:
        guid = item.guid.text
        if 'reuters' in guid and 'http' in guid: # assholes
            toks = guid.split('?')
            tok2 = toks[0].split('/') # take out the GET parameters
            guid = tok2[len(tok2)-1][:-8] # 1) keep last piece of url, 2) take out 8 digits of date lol
        return guid, ''
    elif item.id is not None:
        return item.id.text
    elif item.find('feedburner:origlink') is not None:
        return item.find('feedburner:origlink').text
    elif item.find('link') is not None: # this should be last resort (latimes)
        return item.find('link').text
    return None

def _extractLink(item):
    if item.find('feedburner:origlink') is not None: # this link is usually better ... no redirect
        return item.find('feedburner:origlink').text
    if item.link is not None:
        if item.link.get('href'):
            return item.link.get('href')
        elif item.link.text is not None:
            return item.link.text
    return None

def _extractTitle(item):
    if item.title is not None:
        return item.title.text
    return None
