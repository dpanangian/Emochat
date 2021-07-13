
import pickle
from os.path import abspath, dirname
import pandas as pd
from nltk.tokenize import TweetTokenizer

ROOT_PATH = dirname(dirname(abspath(__file__)))
SVM_MODEL = '{}\model\SVM.pkl'.format(ROOT_PATH)
LR_MODEL = '{}\model\LinearRegression.pkl'.format(ROOT_PATH)
FEATURES_RANKING = '{}\model\\ranked_features.pkl'.format(ROOT_PATH)


def load_model(path):
    loaded_model = pickle.load(open(path, 'rb'))
    return loaded_model

def load_dataframe(dict):
    return pd.DataFrame(dict) 

def tokenize_filter(text):
        tweet_tokenizer = TweetTokenizer()
        tokenized = tweet_tokenizer.tokenize(text)
        top_features = list(set([word for key, value in load_model(FEATURES_RANKING).items() for word in value[-500:] ]))
        return [token for token in tokenized if token in top_features ]


