import torch
from models.bert_model.bert_model import categorize_petition

# Sample petition texts
test_texts = [
    "I need a land ownership certificate for my property.",  # Expected: "Revenue"
    "The drainage system in my area is broken and causing floods.",  # Expected: "Municipal"
    "The government should provide more funds for farmers.",  # Expected: "Revenue"
    "Street lights in my neighborhood are not working.",  # Expected: "Municipal"
]

print("\n🔍 Testing BERT Department Prediction...\n")

for text in test_texts:
    predicted_department = categorize_petition(text)
    print(f"📌 Petition: {text}")
    print(f"✅ Predicted Department: {predicted_department}\n")
