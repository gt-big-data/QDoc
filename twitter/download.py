import twython, json, requests
from tweet import *

class TweetSampler(twython.TwythonStreamer):

    def on_success(self, data):
        if 'text' in data and 'id_str' in data and 'user' in data and 'id_str' in data['user'] and 'timestamp_ms' in data and 'place' in data and 'id' in data['place']:
            time = int(float(data['timestamp_ms']) / 1000.0)
            words, hashtags, mentions = cleanTweet(data['text'])
            longitude = 0
            latitude = 0
            if 'boundingbox' in data['place']:
                bbox = data['place']['bounding_box']['coordinates'][0]
                longitude = ((bbox[0][0]+bbox[2][0])/2.0)
                latitude = ((bbox[0][1]+bbox[1][1])/2.0)
            T = Tweet(data['id_str'], data['text'], data['user']['id_str'], time, longitude, latitude, words, hashtags, mentions)
            saveNewTweet(T)

    def on_error(self, status_code, data):
        print status_code

ATL_BOUNDING_BOX_CORNERS = '-124.92,26.15,-66.59,48.96'

def main():
    with open('credentials.json') as f:
        credentials = json.load(f)
    stream = TweetSampler(
        credentials['APP_KEY'],
        credentials['APP_SECRET'],
        credentials['ACCESS_TOKEN'],
        credentials['ACCESS_TOKEN_SECRET'])
    stream.statuses.filter(locations=ATL_BOUNDING_BOX_CORNERS)

if __name__ == '__main__':
    main()