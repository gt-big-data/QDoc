import twython, json, requests
from tweet import *

class TweetSampler(twython.TwythonStreamer):

    def on_success(self, data):
        if 'text' in data and 'id_str' in data and 'user' in data and 'id_str' in data['user'] and 'name' in data['user'] and 'followers_count' in data['user'] and 'timestamp_ms' in data and 'entities' in data:
            time = int(float(data['timestamp_ms']) / 1000.0)
            hashtags = []
            hashtagsIndices = []
            for hashtag in data['entities']['hashtags']:
                hashtags.append(hashtag['text'])
                hashtagsIndices.append(hashtag['indices'])
            mentions_id = []
            mentions_name = []
            mentionsIndices = []
            for mention in data['entities']['user_mentions']:
                mentions_id.append(mention['id_str'])
                mentions_name.append(mention['name'])
                mentionsIndices.append(mention['indices'])
            urls = []
            urlsIndices = []
            for url in data['entities']['urls']:
                urls.append(url['url'])
                urlsIndices.append(url['indices'])
            words, keywords = summarizeTweet(data['text'], hashtagsIndices, mentionsIndices, urlsIndices)
            favorite_count = 0
            retweet_count = 0
            if 'favorite_count' in data:
                favorite_count = data['favorite_count']
            if 'retweet_count' in data:
                retweet_count = data['retweet_count']
            lon = 0
            lat = 0
            if 'geo' in data and data['geo'] != None and 'coordinates' in data['geo']:
                lat = data['geo']['coordinates'][0]
                lon = data['geo']['coordinates'][1]
            else:
                if 'place' in data and 'bounding_box' in data['place']:
                    bbox = data['place']['bounding_box']['coordinates'][0]
                    lon = (bbox[1][0] + bbox[2][0]) / 2.0
                    lat = (bbox[0][1] + bbox[1][1]) / 2.0
                elif 'location' in data and 'geo' in data['location']:
                    bbox = data['location']['geo']['coordinates'][0]
                    lon = (bbox[1][0] + bbox[2][0]) / 2.0
                    lat = (bbox[0][1] + bbox[1][1]) / 2.0
            T = Tweet(data['id_str'], data['text'], data['user']['id_str'], data['user']['name'], data['user']['followers_count'], time, lon, lat, words, keywords, hashtags, mentions_id, mentions_name, urls, favorite_count, retweet_count)
            saveNewTweet(T)

    def on_error(self, status_code, data):
        print status_code

BOUNDING_BOX = '-124.92,26.15,-66.59,48.96'

def main():
    f = open('credentials.json')
    credentials = json.load(f)
    f.close()
    stream = TweetSampler(
        credentials['APP_KEY'],
        credentials['APP_SECRET'],
        credentials['ACCESS_TOKEN'],
        credentials['ACCESS_TOKEN_SECRET'])
    stream.statuses.filter(language='en',locations=BOUNDING_BOX)

if __name__ == '__main__':
    main()
