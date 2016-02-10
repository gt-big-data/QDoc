# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from dateutil import parser
from datetime import datetime
import pytz, sys, re, time
from article import *
from crawlContent import *
from utils import downloader
import db

def crawlFeed(feedUrl, urlReturn, startStamp=0, toSave=True):
    if 'error' in urlReturn:
        return 'Feed ', feedUrl, ' returned error:', urlReturn['error']
    soup = urlReturn['soup']
    if not toSave:
        f = open('feed.xml', 'w'); f.write(soup.prettify().encode('utf-8')); f.close()

    epoch = datetime(1970, 1, 1).replace(tzinfo=pytz.utc)

    newArticles = []
    latestStamp = startStamp

    items = soup.find_all(['item', 'entry'])
    if len(items) == 0:
        return "No items found"

    for it in items:
        url, error1 = extractLink(it)
        title, error2 = extractTitle(it)
        guid, error3 = extractGuid(it)
        pubtime, error4 = extractPubTime(it)
        errors = ''.join([error1, error2, error3, error4])
        if len(errors) > 0:
            return errors # This exits, there was some error ...
        timestamp = (pubtime - epoch).total_seconds() # Hacky way of going from Datetime object to timestamp
        if timestamp > startStamp: # new article
            latestStamp = max(timestamp, latestStamp)
            newArticles.append({'guid': guid, 'title': title, 'url': url, 'timestamp': timestamp, 'feed': feedUrl})
        else:
            break # we're done, this assumes articles are ordered by descending pubDate

    if toSave:
        db.feed.update({'feed': feedUrl}, {'$set': {'stamp': int(latestStamp), 'lastCrawl': int(time.time())}})
    return newArticles

def extractPubTime(item):
    pubText = ''
    if item.pubdate is not None:
        pubText = item.pubdate.text
    elif item.published is not None:
        pubText = item.published.text
    if pubText == '':
        return datetime.now(), "CANNOT PARSE PUBDATE"
    try:
        trial = parser.parse((re.sub("[\(\[].*?[\)\]]", "", pubText))).replace(tzinfo=pytz.utc)
        return trial, "" # also remove anything between parentheses
    except:
        return "CANNOT PARSE PUBDATE OF", pubText

def extractGuid(item):
    if item.guid is not None:
        guid = item.guid.text
        if 'reuters' in guid and 'http' in guid: # assholes
            toks = guid.split('?')
            tok2 = toks[0].split('/') # take out the GET parameters
            guid = tok2[len(tok2)-1][:-8] # 1) keep last piece of url, 2) take out 8 digits of date lol
        return guid, ''
    elif item.id is not None:
        return item.id.text, ''
    elif item.find('feedburner:origlink') is not None:
        return item.find('feedburner:origlink').text, ''
    elif item.find('link') is not None: # this should be last resort (latimes)
        return item.find('link').text, ''
    return '', 'CANNOT PARSE GUID'

def extractLink(item):
    if item.find('feedburner:origlink') is not None: # this link is usually better ... no redirect
        return item.find('feedburner:origlink').text, ''
    if item.link is not None:
        if item.link.get('href'):
            return item.link.get('href'), ''
        elif item.link.text is not None:
            return item.link.text, ''
    return '', 'CANNOT EXTRACT LINK'

def extractTitle(item):
    if item.title is not None:
        return item.title.text, ''
    return '', 'CANNOT EXTRACT TITLE'

if __name__ == '__main__':
    if len(sys.argv) > 1:
        url = sys.argv[1]
        crawlFeed(url, downloader.getUrl(url), 0, False)
