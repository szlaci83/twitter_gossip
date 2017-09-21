from nltk.sentiment.vader import SentimentIntensityAnalyzer
#from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def analyse(text):
    sid = SentimentIntensityAnalyzer()
    ss = sid.polarity_scores(text)
    return ss['compound']

hotel_rev = ["Great place to be when you are in Bangalore." ,
             "The place was being renovated when I visited so the seating was limited.",
             "Loved the ambience, loved the food",
             "The food is delicious but not over the top.",
             "Service - Little slow, probably because too many people.",
             "The place is not easy to locate",
             "Mushroom fried rice was tasty",
             "really really the worst"]

if __name__ == '__main__':
    for sentence in hotel_rev:
        print(sentence)
        print(analyse(sentence))