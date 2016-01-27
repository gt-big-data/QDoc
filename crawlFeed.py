# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from dateutil import parser
from datetime import datetime
import pytz, sys, re
from article import *
from crawlContent import *
from url2soup import *

def crawlFeed(feedUrl, startStamp, toSave=True):
    # Different types of feeds to handle:
        # Standard:     <item>  http://rss.cnn.com/rss/edition_world.rss
        # Non-standard: <entry> Associated Press: http://hosted2.ap.org/atom/APDEFAULT/3d281c11a96b4ad082fe88aa0db04305

    soup = url2soup(feedUrl)
    if not toSave:
        f = open('feed.xml', 'w'); f.write(soup.prettify().encode('utf-8')); f.close()

    epoch = datetime(1970, 1, 1).replace(tzinfo=pytz.utc)

    newArticles = []
    latestStamp = startStamp

    for it in soup.find_all(['item', 'entry']):
        url = extractLink(it)
        title = extractTitle(it)
        guid = extractGuid(it)
        timestamp = (extractPubTime(it) - epoch).total_seconds() # Hacky way of going from Datetime object to timestamp
        if timestamp > startStamp: # new article
            latestStamp = max(timestamp, latestStamp)
            newArticles.append(Article(guid=guid, title=title, url=url, timestamp=timestamp, feed=feedUrl))
        else:
            break # we're done, this assumes articles are ordered by descending pubDate

    if toSave:
        newArticles = crawlContent(newArticles) # crawls for content
        for article in newArticles:
            article.save()
        print feedUrl, " => +"+str(len(newArticles))
        db.feed.update({'feed': feedUrl}, {'$set': {'stamp': int(latestStamp)}})
    else:
        print "Found ", len(newArticles), " articles"
        print "---------------------------------------"
        for a in newArticles:
            print a.guid.encode('utf8'), "|", a.title.encode('utf8') ,"|", a.timestamp, "|", a.url.encode('utf8')
            print "------------------------------------"

def extractPubTime(item):
    pubText = ''
    if item.pubdate is not None:
        pubText = item.pubdate.text
    elif item.published is not None:
        pubText = item.published.text
    if pubText == '':
        print "[PROBLEM] CANNOT PARSE PUBDATE"
    return parser.parse((re.sub("[\(\[].*?[\)\]]", "", pubText))).replace(tzinfo=pytz.utc) # also remove anything between parentheses

def extractGuid(item):
    if item.guid is not None:
        guid = item.guid.text
        if 'reuters' in guid and 'http' in guid: # assholes
            toks = guid.split('?')
            tok2 = toks[0].split('/') # take out the GET parameters
            guid = tok2[len(tok2)-1][:-8] # 1) keep last piece of url, 2) take out 8 digits of date lol
        return guid
    elif item.id is not None:
        return item.id.text
    elif item.find('feedburner:origlink') is not None:
        return item.find('feedburner:origlink').text
    elif item.find('link') is not None: # this should be last resort (latimes)
        return item.find('link').text
    print "[PROBLEM] CANNOT PARSE GUID"
    return ''

def extractLink(item):
    if item.find('feedburner:origlink') is not None: # this link is usually better ... no redirect
        return item.find('feedburner:origlink').text
    if item.link is not None:
        if item.link.get('href'):
            return item.link.get('href')
        elif item.link.text is not None:
            return item.link.text
    print "[PROBLEM] CANNOT PARSE URL"    
    return ''

def extractTitle(item):
    if item.title is not None:
        return item.title.text
    print "[PROBLEM] CANNOT PARSE TITLE"
    return ''

if __name__ == '__main__':
    if len(sys.argv) > 1:
        url = sys.argv[1]
        crawlFeed('test', url, False)