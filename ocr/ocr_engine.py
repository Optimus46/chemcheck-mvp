import pytesseract
from PIL import Image

def extract_text(image_file):
    image = Image.open(image_file)
    text = pytesseract.image_to_string(image)
    return text
