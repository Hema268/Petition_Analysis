import os
import pytesseract
import torch  # PyMuPDF for PDF text extraction
from PIL import Image
from flask import Flask, request, jsonify
from flask_cors import CORS
from database.db_connection import get_db_connection
from utils.text_preprocessing import preprocess_text
from utils.notification import send_notification
from models.bert_model.bert_model import categorize_petition
from models.random_forest.random_forest import detect_urgency
from models.kmeans_clustering.kmeans_clustering import detect_repetitive_issues
from models.lstm_sentiment.lstm_sentiment import analyze_sentiment

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend communication

# Configure upload folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Database connection
db = get_db_connection()
if db is None:
    print("⚠ MySQL Connection not available. Check credentials and MySQL server status.")

# Set the path where Tesseract-OCR is installed (Windows Users)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ✅ Load fine-tuned BERT Model properly
try:
    from transformers import BertTokenizer, BertForSequenceClassification

    BERT_MODEL_PATH = "models/bert_model"

    print("✅ Loading updated BERT tokenizer...")
    TOKENIZER = BertTokenizer.from_pretrained(BERT_MODEL_PATH)

    print("✅ Loading updated BERT model...")
    DEVICE = torch.device("cpu")  # Use CPU for inference
    MODEL = BertForSequenceClassification.from_pretrained(BERT_MODEL_PATH)

    MODEL.load_state_dict(torch.load(f"{BERT_MODEL_PATH}/pytorch_model.bin", map_location=DEVICE))
    MODEL.to(DEVICE)
    MODEL.eval()

    print("✅ Fine-tuned BERT Model Loaded Successfully!")

except Exception as e:
    print(f"❌ Error loading BERT model: {e}")
    MODEL = None
    TOKENIZER = None

users = {
    "admin": {"password": "1234", "department": "Revenue"},
    "user1": {"password": "abcd", "department": "Municipal"},
}

def extract_text_from_file(file_path):
    """Extracts text from images or PDFs."""
    try:
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            image = Image.open(file_path)
            return pytesseract.image_to_string(image).strip()
        elif file_path.lower().endswith('.pdf'):
            text = ""
            pdf = fitz.open(file_path)
            for page in pdf:
                text += page.get_text("text")
            return text.strip()
        else:
            return None  # Unsupported file type
    except Exception as e:
        print(f"❌ Error extracting text: {e}")
        return None


@app.route("/")
def home():
    return "Flask API is running!"

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username in users and users[username]["password"] == password:
        department = users[username]["department"]
        return jsonify({"success": True, "department": department, "message": "Login successful!"})
    else:
        return jsonify({"success": False, "message": "Invalid username or password"}), 401


@app.route('/api/petitions', methods=['GET'])
def get_petitions():
    """Fetch all petitions from the database."""
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM petitions")
        petitions = cursor.fetchall()
        return jsonify(petitions), 200
    except Exception as e:
        print(f"❌ Error in get_petitions: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/petitions', methods=['POST'])
def submit_petition():
    """Handles petition submission: Upload, extract text, categorize, and store."""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files['file']
        phone_number = request.form.get('phone_number')
        name = request.form.get('name')  # Get the name from form data

        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)

        # Extract text from uploaded file
        extracted_text = extract_text_from_file(file_path)
        if not extracted_text:
            return jsonify({"error": "Failed to extract text"}), 400

        # Preprocess petition content
        processed_content = preprocess_text(extracted_text)

        # Predict department using fine-tuned BERT Model
        department = categorize_petition(processed_content)

        # Detect urgency using Random Forest
        try:
            urgency = detect_urgency(processed_content) 
        except Exception as e:
            urgency = "urgent"
            print(f"❌ Error in detect_urgency: {e}")

        # Detect repetitive issues using K-Means
        try:
            clusters = detect_repetitive_issues([processed_content])
            cluster_label = str(clusters[0]) if clusters else "Unknown"
        except Exception as e:
            cluster_label = "error"
            print(f"❌ Error in detect_repetitive_issues: {e}")

        # Analyze sentiment using LSTM
        try:
            sentiment = str(analyze_sentiment(processed_content))
        except Exception as e:
            sentiment = "error"
            print(f"❌ Error in analyze_sentiment: {e}")

        # Save petition to database
        cursor = db.cursor()
        query = """
            INSERT INTO petitions (file_name, file_path, extracted_text, department, priority, cluster, sentiment, phone_number)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (file.filename, file_path, processed_content, department, urgency, cluster_label, sentiment, phone_number))
        db.commit()

        # Send notification with name included
        send_notification(f"Hello {name}, your petition '{file.filename}' has been successfully submitted under '{department}'.", phone_number)

        return jsonify({
            "message": "Petition submitted successfully!",
            "file": file.filename,
            "department": department,
            "urgency": urgency,
            "cluster": cluster_label,
            "sentiment": sentiment,
            "phone_number": phone_number
        }), 201

    except Exception as e:
        print(f"❌ Error in submit_petition: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/petitions/<int:petition_id>/status', methods=['PUT'])
def update_status(petition_id):
    """Update the status of a petition and notify the user."""
    try:
        data = request.get_json()
        new_status = data.get('status')

        if new_status not in ['pending', 'in_progress', 'resolved']:
            return jsonify({"error": "Invalid status"}), 400

        cursor = db.cursor()
        cursor.execute("SELECT phone_number, department FROM petitions WHERE id = %s", (petition_id,))
        result = cursor.fetchone()

        if not result:
            return jsonify({"error": "Petition not found"}), 404

        phone_number, department = result

        cursor.execute("UPDATE petitions SET status = %s WHERE id = %s", (new_status, petition_id))
        db.commit()

        message = f"Your petition (ID: {petition_id}) under '{department}' has been updated to '{new_status}'."
        send_notification(message, phone_number)

        return jsonify({"message": "Petition status updated successfully!", "phone_number": phone_number}), 200

    except Exception as e:
        print(f"❌ Error in update_status: {e}")
        return jsonify({"error": str(e)}), 500

# Route to delete a petition
@app.route('/api/petitions/<int:petition_id>', methods=['DELETE'])
def delete_petition(petition_id):
    try:
        cursor = db.cursor()
        cursor.execute("DELETE FROM petitions WHERE id = %s", (petition_id,))
        db.commit()

        return jsonify({"message": "Petition deleted successfully!"}), 200

    except Exception as e:
        print(f"❌ Error in delete_petition: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
