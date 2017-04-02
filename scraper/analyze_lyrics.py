from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import sys

if(len(sys.argv) == 0):
    print("Select an artist")
    exit()


def get_sentiment(artist, filename):
    path = 'Artists/' + artist + '/lyrics/'
    f = open(path + filename, "r")
    raw_text = f.read()

    # Using already trained
    sid = SentimentIntensityAnalyzer(lexicon_file='/Users/bencongdon/nltk_data/sentiment/vader_lexicon/vader_lexicon.txt')
    sentences = tokenize.sent_tokenize(raw_text)
    scores = dict([('pos', 0), ('neu', 0), ('neg', 0), ('compound', 0)])
    for sentence in sentences:
        ss = sid.polarity_scores(sentence)
        for k in sorted(ss):
            scores[k] += ss[k]
    f.close()
    return scores
