import pytesseract
from PIL import Image

def extract_text_from_image(image_path):
    """
    Extract text from an image using Tesseract OCR.
    
    Args:
        image_path (str): Path to the image file.
    
    Returns:
        str: Extracted text.
    """
    try:
        # Open the image
        image = Image.open(image_path)
        # Extract text using Tesseract OCR
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"Error extracting text from image: {e}")
        return None