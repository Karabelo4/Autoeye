import cv2
import easyocr
import numpy as np

reader = easyocr.Reader(['en'])

def detect_license_plate(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Read text from image using OCR
    results = reader.readtext(gray)
    
    for (bbox, text, prob) in results:
        if prob > 0.5:  # Confidence threshold
            return text
    return None
