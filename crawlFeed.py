# -*- coding: utf-8 -*-
from urllib import urlopen
from bs4 import BeautifulSoup
from dateutil import parser
from datetime import datetime
import pytz, sys
from stamps import * # saving last stamps
from article import *
from crawlContent import *
from url2soup import *

def crawlFeed(source, feedName, feedUrl, toSave=True):
    """Crawl an RSS feed.
    Arguments:
    source -- Main name of the news site (e.g. cnn, nyt, etc.).
    feedName -- The title of the RSS feed (e.g. 'cnn_world', 'cnn_sport').
    feedUrl -- An RSS feed url to extract links from (e.g. 'http://*.rss').
    toSave -- Whether to save to the database or not (maybe it's a test).
    """
    # Different types of feeds to hadle:
        # Standard:     <item>  http://rss.cnn.com/rss/edition_world.rss
        # Non-standard: <entry> Associated Press: http://hosted2.ap.org/atom/APDEFAULT/3d281c11a96b4ad082fe88aa0db04305

    startStamp = loadLastStamp(feedName)
    soup = url2soup(feedUrl)
    if not toSave:
        f = open('feed.xml', 'w'); f.write(soup.prettify().encode('utf-8')); f.close()

    epoch = datetime(1970, 1, 1).replace(tzinfo=pytz.utc)

    latestStamp = startStamp
    newArticles = []

    for it in soup.find_all(['item', 'entry']):
        url = extractLink(it)
        title = extractTitle(it)
        guid = extractGuid(it, source)
        timestamp = (extractPubTime(it) - epoch).total_seconds() # Hacky way of going from Datetime object to timestamp
        if timestamp > startStamp: # new article
            latestStamp = max(timestamp, latestStamp)
            newArticles.append(Article(guid=guid, title=title, url=url, timestamp=timestamp, source=source, feed=feedName))
        else:
            break # we're done, this assumes articles are ordered by descending pubDate

    if toSave:
        newArticles = crawlContent(newArticles) # crawls for content
        for article in newArticles:
            article.save()
        print feedName, " => +"+str(len(newArticles))
        saveLastStamp(feedName, latestStamp) # save to not reload articles
    else:
        print "Found ", len(newArticles), " articles"
        print "---------------------------------------"
        for a in newArticles:
            print a.guid, "|", a.title,"|", a.timestamp, "|", a.url
            print "------------------------------------"

def extractPubTime(item):
    pubText = ''
    if item.pubdate is not None:
        pubText = item.pubdate.text
    elif item.published is not None:
        pubText = item.published.text
    if pubText == '':
        print "[PROBLEM] CANNOT PARSE PUBDATE"
    return parser.parse(pubText).replace(tzinfo=pytz.utc)

def extractGuid(item, source):
    if item.guid is not None:
        guid = item.guid.text
        if source == 'reuters' and 'http' in guid: # assholes
            toks = guid.split('?')
            tok2 = toks[0].split('/') # take out the GET paramaters
            guid = tok2[len(tok2)-1][:-8] # 1) keep last piece of url, 2) take out 8 digits of date lol
        return guid
    elif item.id is not None:
        return item.id.text
    print "[PROBLEM] CANNOT PARSE GUID"
    return ''

def extractLink(item):
    if item.link is not None:
        if item.link.get('href'):
            return item.link.get('href')
        elif item.link.text is not None:
            return item.link.text
    elif item.find('feedburner:origlink') is not None:
        return item.find('feedburner:origlink').text
    print "[PROBLEM] CANNOT PARSE URL"    
    return ''

def extractTitle(item):
    if item.title is not None:
        return item.title.text
    print "[PROBLEM] CANNOT PARSE TITLE"
    return ''

if __name__ == '__main__':
    url = 'http://rss.cnn.com/rss/edition_world.rss'
    if len(sys.argv) > 1:
        url = sys.argv[1]
    crawlFeed('test', 'test', url, False)