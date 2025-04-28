import torch
from transformers import BertTokenizer, BertForSequenceClassification

# Define the model path
MODEL_PATH = "models/bert_model"

try:
    print("✅ Loading local BERT tokenizer...")
    TOKENIZER = BertTokenizer.from_pretrained(MODEL_PATH)

    print("✅ Loading local BERT model...")
    DEVICE = torch.device("cpu")  # Use CPU for inference
    MODEL = BertForSequenceClassification.from_pretrained(MODEL_PATH)

    # Manually load the state dictionary
    MODEL.load_state_dict(torch.load(f"{MODEL_PATH}/pytorch_model.bin", map_location=DEVICE))

    MODEL.to(DEVICE)
    MODEL.eval()  # Set model to evaluation mode

    print("✅ BERT Model and Tokenizer Loaded Successfully!")

except Exception as e:
    print(f"❌ Error loading BERT model/tokenizer: {e}")
    TOKENIZER = None
    MODEL = None

# Function to categorize petitions
def categorize_petition(text):
    """Predict the department from extracted petition text."""
    if TOKENIZER is None or MODEL is None:
        print("❌ BERT model is not loaded properly. Returning default category.")
        return "General Inquiry"

    try:
        # Tokenize input text
        inputs = TOKENIZER(text, return_tensors="pt", truncation=True, padding=True, max_length=512).to(DEVICE)

        # Run model inference
        with torch.no_grad():
            outputs = MODEL(**inputs)

        # Get predicted department index
        predicted_class = torch.argmax(outputs.logits, dim=1).item()

        # Label mapping
        label_mapping = {0: "Revenue department", 1: "Municipal department"}
        return label_mapping.get(predicted_class, "Unknown")  # Default to "Unknown" if index is wrong

    except Exception as e:
        print(f"❌ Error in categorize_petition: {e}")
        return "General Inquiry"  # Default fallback
