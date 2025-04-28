import joblib
import os
import numpy as np

# Define paths for model files
model_path = r"E:\Final_yr_Project\petition-analysis-system\backend\models\random_forest\random_forest_model.pkl"
vectorizer_path = r"E:\Final_yr_Project\petition-analysis-system\backend\models\random_forest\tfidf_vectorizer.pkl"
encoder_path = r"E:\Final_yr_Project\petition-analysis-system\backend\models\random_forest\label_encoder.pkl"

# Ensure all files exist
if not all(os.path.exists(path) for path in [model_path, vectorizer_path, encoder_path]):
    raise FileNotFoundError("One or more model files not found!")

# Load the trained components
model = joblib.load(model_path)
vectorizer = joblib.load(vectorizer_path)
label_encoder = joblib.load(encoder_path)  # Load the Label Encoder

def detect_urgency(text):
    """
    Detect the urgency level of a petition using Random Forest.
    
    Args:
        text (str): The content of the petition.
    
    Returns:
        str: The predicted urgency level ('low', 'normal', or 'high').
    """
    try:
        # Ensure text is valid
        if not isinstance(text, str) or text.strip() == "":
            print("⚠️ Invalid text input, defaulting urgency to 'high' (urgent)")
            return "high"  # Default to high urgency

        # Transform input text using TF-IDF vectorizer
        features = vectorizer.transform([text])

        # Predict urgency (returns numerical label)
        prediction = model.predict(features)

        # Decode numerical label back to 'urgent' or 'non-urgent'
        urgency_label = label_encoder.inverse_transform(prediction)[0]  # Convert back to original label

        # Map to database ENUM values
        urgency_mapping = {"urgent": "high", "non-urgent": "normal"}
        priority = urgency_mapping.get(urgency_label, "high")  # Default to 'high' if not found

        print(f"🔍 Model prediction: {prediction[0]} → Classified as: {urgency_label} → Mapped to: {priority}")
        return priority

    except Exception as e:
        print(f"❌ Error in detect_urgency: {e}")
        return "high"  # Default to high urgency to prevent database issues
