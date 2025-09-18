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

    def clean_review(self, text: str):
        review = re.sub('[^a-zA-Z]', ' ', text)
        review = review.lower().split()
        review = [self.ps.stem(word) for word in review if word not in self.stop_words]

        return ' '.join(review)

    def load_and_prepare(self):
        dataset = pd.read_csv(self.dataset_path, delimiter = '\t', quoting = 3)
        cleaned_reviews = [self.clean_review(review) for review in dataset['Review']]

        X = self.cv.fit_transform(cleaned_reviews).toarray()
        y = dataset.iloc[:, -1].values
        return X, y
    
    def train_model(self):
        X, y = self.load_and_prepare()
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)
        self.classifier.fit(X_train, y_train)

        y_pred = self.classifier.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Model trained with accuracy: {accuracy:.2f}")

        
