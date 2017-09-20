from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json, pprint

import sentiment

#Dict from JSON that contains the user credentials to access Twitter API
properties = json.loads(open('properties.json').read())

class StdOutListener(StreamListener):
    pp = pprint.PrettyPrinter(indent=4)

    def on_data(self, data):
        tweetJSON = json.loads(data)
        try:
            print((tweetJSON['text'], tweetJSON['lang'], str(tweetJSON['user']['followers_count']), tweetJSON['timestamp_ms'], sentiment.analyse(tweetJSON['text']) ))
        except KeyError:
            pass
       # self.pp.pprint(tweetJSON)
        return True

    def on_error(self, status):
        print(status)

def filterStream(keywordList):
    # This handles Twitter authetification and the connection to Twitter Streaming API
    auth = OAuthHandler(properties["consumer_key"], properties["consumer_secret"])
    auth.set_access_token(properties["access_token"], properties["access_token_secret"])
    stream = Stream(auth, StdOutListener())

    # This line filter Twitter Streams to capture data by the keywords:
    stream.filter(track=keywordList, async=True)

if __name__ == '__main__':
    theFilter = ['bitcoin']
    print("Twitter streaming API filtering for " + str(theFilter))
    filterStream(theFilter)