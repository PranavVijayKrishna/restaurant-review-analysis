import re
import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score


class SentimentModel:
    def __init__(self, dataset_path = "Restaurant_Reviews.tsv"):
        self.dataset_path = dataset_path
        self.cv = CountVectorizer(max_features = 1500)
        self.classifier = GaussianNB()
        self.ps = PorterStemmer()
        self.stop_words = set(stopwords.words('english'))
        self.stop_words.discard('not')
