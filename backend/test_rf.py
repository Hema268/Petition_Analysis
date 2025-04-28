import joblib
import os

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
label_encoder = joblib.load(encoder_path)

def detect_urgency(text):
    """
    Detect the urgency level of a petition using Random Forest.
    
    Args:
        text (str): The content of the petition.
    
    Returns:
        str: The predicted urgency level ('urgent' or 'non-urgent').
    """
    try:
        # Ensure text is valid
        if not isinstance(text, str) or text.strip() == "":
            print(f"⚠️ Invalid text input: '{text}', defaulting to 'urgent'")
            return "urgent"  # Default to urgent

        # Transform input text using TF-IDF vectorizer
        features = vectorizer.transform([text])

        # Predict urgency (returns numerical label)
        prediction = model.predict(features)

        # Decode numerical label back to 'urgent' or 'non-urgent'
        urgency = label_encoder.inverse_transform(prediction)[0]

        print(f"🔍 Input: {text}\n✅ Predicted Urgency: {urgency}\n")
        return urgency

    except Exception as e:
        print(f"❌ Error in detect_urgency: {e}")
        return "urgent"  # Default in case of error

# 🚀 Test Cases
test_cases = [
    ("Urgent matter regarding sewage overflow in our neighborhood. Please act immediately!", "urgent"),
    ("There is an issue with the streetlight, it has been broken for a while now.", "non-urgent"),
    ("Request for property tax correction. The amount charged seems incorrect compared to my neighbors.", "non-urgent"),
    ("", "urgent"),  # Empty input should default to 'urgent'
    ("    ", "urgent"),  # Whitespace input should default to 'urgent'
    (None, "urgent"),  # None input should default to 'urgent'
]


# Running test cases
print("\n🔎 Running Test Cases for Random Forest Urgency Model:\n" + "-"*60)
for text, expected in test_cases:
    result = detect_urgency(text)
    print(f"📝 Expected: {expected} | 🚀 Model Output: {result}\n" + "-"*60)

# Final check
print("\n✅ Model Testing Completed! If outputs match expected results, the model is working correctly.")
