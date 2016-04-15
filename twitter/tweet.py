from nltk.corpus import stopwords
from collections import namedtuple
from dbco import *

global cacheToSave
cacheToSave = []

stopW = set(stopwords.words('english'))
commW = []
commW.extend(stopW)
common_words = set(commW)

Tweet = namedtuple('Tweet', ['guid', 'text', 'author_id', 'author_name', 'author_followers_count', 'timestamp', 'lon', 'lat', 'words', 'keywords', 'hashtags', 'mentions_id', 'mentions_name', 'urls', 'favorite_count', 'retweet_count'])
class Tweet(namedtuple('Tweet', ['guid', 'text', 'author_id', 'author_name', 'author_followers_count', 'timestamp', 'lon', 'lat', 'words', 'keywords', 'hashtags', 'mentions_id', 'mentions_name', 'urls', 'favorite_count', 'retweet_count'])):
    def __new__(cls, guid, text, author_id, author_name, author_followers_count, timestamp, lon, lat, words, keywords, hashtags, mentions_id, mentions_name, urls, favorite_count, retweet_count):
        return super(Tweet, cls).__new__(cls, guid, text, author_id, author_name, author_followers_count, timestamp, lon, lat, words, keywords, hashtags, mentions_id, mentions_name, urls, favorite_count, retweet_count)

def sendCache():
    global cacheToSave
    tweetInsert = db.tweet.initialize_unordered_bulk_op()
    for T in cacheToSave:
        tweetInsert.insert(T)
    tweetInsert.execute()
    cacheToSave = []

def saveNewTweet(T):
    global cacheToSave
    if isValid(T):
        cacheToSave.append(T._asdict())
    if len(cacheToSave) >= 100:
        sendCache()

def summarizeTweet(text, hashtagsIndices, mentionsIndices, urlsIndices):
    global common_words
    startPoints = []
    endPoints = []
    for hIndices in hashtagsIndices:
        startPoints.append(hIndices[0])
        endPoints.append(hIndices[1] - 1)
    for mIndices in mentionsIndices:
        startPoints.append(mIndices[0])
        endPoints.append(mIndices[1] - 1)
    for uIndices in urlsIndices:
        startPoints.append(uIndices[0])
        endPoints.append(uIndices[1] - 1)
    tweetString = ""
    buf = ""
    for i in range(len(text)):
        if i in startPoints:
            tweetString += buf
        elif i in endPoints:
            buf = ""
        else:
            if ord(text[i]) < 128:
                if text[i] == '\n' or text[i] == '(' or text[i] == ')' or text[i] == '!' or text[i] == '.' or text[i] == ',' or text[i] == ';' or text[i] == '\"' or text[i] == '?' or text[i] == '&' or text[i] == '~' or text[i] == ':' or text[i] == '/':
                    buf += ' '
                else:
                    buf += text[i]
    tweetString += buf
    rawwords = tweetString.split(' ')
    words = []
    for word in rawwords:
        if word != "":
            words.append(word.lower())
    keywords = list(set(words)-common_words)
    return words, keywords

def insertTweet(T):
    db.tweet.update_one({'guid': T['guid']}, {'$set': T}, upsert=True)

def isValid(t):
    if len(t.words) + len(t.hashtags) + len(t.mentions_id) < 3:
        return False
    return True