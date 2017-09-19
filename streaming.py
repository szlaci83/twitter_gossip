from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json, pprint

#Dict from JSON that contains the user credentials to access Twitter API
properties = json.loads(open('properties.json').read())

class StdOutListener(StreamListener):
    pp = pprint.PrettyPrinter(indent=4)

    def on_data(self, data):
        self.pp.pprint(data)
        return True

    def on_error(self, status):
        print(status)

def filterStream(keywordList):
    # This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(properties["consumer_key"], properties["consumer_secret"])
    auth.set_access_token(properties["access_token"], properties["access_token_secret"])
    stream = Stream(auth, l)

    # This line filter Twitter Streams to capture data by the keywords:
    stream.filter(track=keywordList)


if __name__ == '__main__':
    filterStream(['EUR', 'GBP'])