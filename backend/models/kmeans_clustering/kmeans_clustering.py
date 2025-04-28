from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

# Load pre-trained K-Means model and TF-IDF vectorizer
model = joblib.load(r"E:\Final_yr_Project\petition-analysis-system\backend\models\kmeans_clustering\kmeans_model.pkl")
vectorizer = joblib.load(r"E:\Final_yr_Project\petition-analysis-system\backend\models\kmeans_clustering\tfidf_vectorizer.pkl")

def detect_repetitive_issues(texts):
    """
    Detect repetitive grievances by clustering similar petitions.
    
    Args:
        texts (list): List of petition contents.
    
    Returns:
        list: Cluster labels for each petition.
    """
    # Vectorize texts using TF-IDF
    tfidf_matrix = vectorizer.transform(texts)
    
    # Predict clusters using K-Means
    clusters = model.predict(tfidf_matrix)
    return clusters