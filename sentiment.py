#!/usr/bin/python
#from nltk.sentiment.vader import SentimentIntensityAnalyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

sid = SentimentIntensityAnalyzer()

def analyse(text):
    ss = sid.polarity_scores(text)
    return ss.get('compound', None)

if __name__ == '__main__':
    hotel_rev = ["Great place to be when you are in Bangalore." ,
             "The place was being renovated when I visited so the seating was limited.",
             "Loved the ambience, loved the food",
             "The food is delicious but not over the top.",
             "Service - Little slow, probably because too many people.",
             "The place is not easy to locate",
             "Mushroom fried rice was tasty",
             "really really the worst"]
    for sentence in hotel_rev:
        print(sentence)
        print(analyse(sentence))
