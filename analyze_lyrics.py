from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re
import sys

if(len(sys.argv) == 0):
    print("Select an artist")
    exit()


def get_sentiment(song):

    raw_text = song
    raw_text = re.sub("\n", ". ", str(raw_text))

    # Using already trained
    sid = SentimentIntensityAnalyzer()
    sentences = tokenize.sent_tokenize(raw_text)

    scores = dict([('pos', 0), ('neu', 0), ('neg', 0), ('compound', 0)])
    for sentence in sentences:

        ss = sid.polarity_scores(sentence)

        for k in sorted(ss):
            scores[k] += ss[k]

    return scores
