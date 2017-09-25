#!/usr/bin/python
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json, pprint, time, gzip, os

import sentiment

#Dict from JSON that contains the user credentials to access Twitter API
properties = json.loads(open('properties.json').read())

the_filter = ['bitcoin', 'ethereum', 'ETH', 'BTC']

class StdOutListener(StreamListener):
    pp = pprint.PrettyPrinter(indent=4)
    no_of_tweets = 0
    total_sentiment_score = 0
    today = time.localtime(time.time())[7]

    def moveToZip(self, file_num):
        now = time.localtime(time.time() - 5000)
        date = str(now[0]) + '-' + str(now[1]) + '-' + str(now[2])
        f_in = open('tweets-' + str(file_num) +'.json', 'rb')
        f_out = gzip.open('tweets-' + date +'.json.gz', 'wb')
        f_out.writelines(f_in)
        f_out.close()
        f_in.close()
        os.remove('tweets-' + str(file_num) +'.json')

    def save_as_JSON(self, data, file_num):
        with open('tweets-' + str(file_num) + '.json', 'a') as outfile:
            outfile.write(json.dumps(data, indent=4,sort_keys=True))
            outfile.write("\n")
            outfile.close()

    def on_data(self, data):
        tweetJSON = json.loads(data)
        lineJSON = {}

        try:
            sentiment_line = tweetJSON['text']
            lineJSON['text'] = tweetJSON['text']
            lineJSON['followers_count'] = tweetJSON['user']['followers_count']
            lineJSON['timestamp_ms'] = tweetJSON['timestamp_ms']
            lineJSON['text'] = tweetJSON['text']
        except KeyError:
            pass
            sentiment_line = ""
        sentiment_score = sentiment.analyse(sentiment_line)
        lineJSON['sentiment'] = sentiment_score
        self.pp.pprint(lineJSON)
        now = time.localtime(time.time())[7]
        if self.today != now:
            self.moveToZip(self.today)
            self.today = now
        self.save_as_JSON(lineJSON, self.today)
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

def do_filter():
    print("Twitter streaming API filtering for " + str(the_filter))
    filterStream(the_filter)

if __name__ == '__main__':
    crypto_filter = ['bitcoin', 'ethereum', 'ETH', 'BTC']
    do_filter(crypto_filter)