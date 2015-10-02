from urllib import urlopen
from bs4 import BeautifulSoup

from pymongo import MongoClient, errors

from dateutil import parser
from datetime import datetime
import time
import pytz

from stamps import * # saving last stamps

from article import *
from crawlContent import *

def crawlFeed(source, feedName, feedUrl):
    """Crawl an RSS feed.

    Arguments:
    source -- Main name of the news site (e.g. cnn, nyt, etc.).
    feedName -- The title of the RSS feed (e.g. 'cnn_world', 'cnn_sport').
    feedUrl -- An RSS feed url to extract links from (e.g. 'http://*.rss').
    """

    # Given a feedname from a Source and a URL of where the Rss feed is,
    # Get the new articles, with their basic params: Title, URL, Publish Time
    # loadLastStamp always returns 0.
    startStamp = loadLastStamp(feedName)
    html = urlopen(feedUrl).read()

    db.html.update({'name': feedName}, {'html': html, 'name':feedName}, upsert=True)

    epoch = datetime(1970, 1, 1).replace(tzinfo=pytz.utc)

    soup = BeautifulSoup(html, 'html.parser')
    latestStamp = startStamp
    newArticles = []

    for it in soup.find_all('item'):
        dt = extractPubTime(it)
        guid = extractGuid(it, source)
        timestamp = (dt - epoch).total_seconds() # Hacky way of going from Datetime object to timestamp
        if timestamp > startStamp: # new article
            latestStamp = max(timestamp, latestStamp)
            url = extractLink(it)
            newArticles.append(Article(guid=guid, title=it.title.text, url=url, timestamp=timestamp, source=source, feed=feedName))
        else:
            break # we're done, this assumes articles are ordered by descending pubDate

    newArticles = crawlContent(newArticles) # crawls for content, img and possible keywords (?)
    saveNewArticles(newArticles) # save to Database
    print feedName, " => +"+str(len(newArticles))

    saveLastStamp(feedName, latestStamp) # save to not reload articles

def extractPubTime(item):
    """Create a DateTime object from a BeautifulSoup object that's probably a date.

    Arguments:
    item -- A soup object.
    """
    dt = parser.parse(item.pubdate.text) # string to Datetime
    return dt.replace(tzinfo=pytz.utc)

def extractGuid(item, source):
    """Extract a GUID from the HTML source.

    Every unique article needs a unique GUID. If two articles have the same GUID, they are
    considered to be the same.
    """
    guidItem = item.find('guid')
    if guidItem is not None:
        guid = guidItem.text
        if source == 'reuters' and 'http' in guid: # assholes
            toks = guid.split('?')
            tok2 = toks[0].split('/') # take out the GET paramaters
            guid = tok2[len(tok2)-1][:-8] # 1) keep last piece of url, 2) take out 8 digits of date lol
        return guid
    return ''

def extractLink(item):
    """Extract a canonical link from the article.

    Arguments:
    item -- A BeautifulSoup object.
    """
    t1 = item.find('feedburner:origlink')
    t2 = item.find('link')
    if t1 is not None:
        return t1.text
    elif t2 is not None:
        return t2.text
    return ''
