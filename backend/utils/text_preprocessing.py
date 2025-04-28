import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk

nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text):
    """
    Preprocess the text by cleaning, tokenizing, and removing stopwords.
    
    Args:
        text (str): The input text.
    
    Returns:
        str: The preprocessed text.
    """
    # Convert to lowercase
    text = text.lower()
    # Remove special characters
    text = re.sub(r'\W', ' ', text)
    # Tokenize text
    tokens = word_tokenize(text)
    # Remove stopwords
    tokens = [word for word in tokens if word not in stopwords.words('english')]
    return ' '.join(tokens)