import unittest
from backend.models.bert_model.bert_model import categorize_petition
from backend.models.random_forest.random_forest import detect_urgency
from backend.models.kmeans_clustering.kmeans_clustering import detect_repetitive_issues
from backend.models.lstm_sentiment.lstm_sentiment import analyze_sentiment

class TestModels(unittest.TestCase):
    def test_bert_categorization(self):
        category = categorize_petition("The road near my house is damaged.")
        self.assertIn(category, range(10))

    def test_random_forest_urgency(self):
        urgency = detect_urgency("The road near my house is damaged.")
        self.assertIn(urgency, ["low", "medium", "high"])

    def test_kmeans_clustering(self):
        clusters = detect_repetitive_issues(["The road near my house is damaged."])
        self.assertIsInstance(clusters, list)

    def test_lstm_sentiment(self):
        sentiment = analyze_sentiment("The road near my house is damaged.")
        self.assertIn(sentiment, ["positive", "negative"])

if __name__ == '__main__':
    unittest.main()