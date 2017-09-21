from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json, pprint

import sentiment

#Dict from JSON that contains the user credentials to access Twitter API
properties = json.loads(open('properties.json').read())

class StdOutListener(StreamListener):
    pp = pprint.PrettyPrinter(indent=4)
    no_of_tweets = 0
    total_sentiment_score = 0

    def save_as_JSON(self, data):
        with open('tweets.json', 'a', encoding="utf8") as outfile:
            outfile.write(json.dumps(data, indent=4,sort_keys=True))
            outfile.write("\n")
            outfile.close()

    def on_data(self, data):
        tweetJSON = json.loads(data)
        lineJSON = {}
        sentiment_score = sentiment.analyse(tweetJSON['text'])

        try:
            lineJSON['text'] = tweetJSON['text']
            lineJSON['followers_count'] = tweetJSON['user']['followers_count']
            lineJSON['timestamp_ms'] = tweetJSON['timestamp_ms']
            lineJSON['text'] = tweetJSON['text']
            lineJSON['sentiment'] = sentiment_score
        except KeyError:
            pass
        self.pp.pprint(lineJSON)
        self.save_as_JSON(lineJSON)
        if sentiment_score != 0 :
            self.no_of_tweets +=1
            self.total_sentiment_score += sentiment_score
        try:
            print("AVG sentiment: " + str(self.total_sentiment_score / self.no_of_tweets))
        except ZeroDivisionError:
            pass
        return True

    def on_error(self, status):
        print(status)

def filterStream(keywordList):
    # This handles Twitter authetification and the connection to Twitter Streaming API
    auth = OAuthHandler(properties["consumer_key"], properties["consumer_secret"])
    auth.set_access_token(properties["access_token"], properties["access_token_secret"])
    stream = Stream(auth, StdOutListener())

    # This line filter Twitter Streams to capture data by the keywords:
    stream.filter(track=keywordList)

if __name__ == '__main__':
    theFilter = ['bitcoin']
    print("Twitter streaming API filtering for " + str(theFilter))
    filterStream(theFilter)