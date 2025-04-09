from pdf2image import convert_from_path
import pytesseract
from pytesseract import Output
import numpy as np
import cv2
import pandas as pd
import requests
import os

POPPLER_PATH = r"C:\Program Files\poppler-24.08.0\Library\bin"
KEYWORD = "energy and carbon report"

df = pd.read_csv("filing_history.csv") # Generated using ch-filings-list.py

links = []
carbon_page = []

# OCR-based keyword search
def find_keyword_page_via_ocr(pdf_path, keyword, poppler_path):
    pages = convert_from_path(pdf_path, dpi=300, poppler_path=poppler_path)
    print(f"Scanning {pdf_path}")
    for i, image in enumerate(pages):
        print(f"OCR scanning page {i+1}...")
        gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
        text = pytesseract.image_to_string(gray)
        if keyword.lower() in text.lower():
            print(f"Keyword found on page {i+1}")
            carbon_page.append(i + 1)
            return i, pages
    print("Keyword not found in OCR text.")
    carbon_page.append(0)
    return None, pages


# Iteratation
for index, row in df.iterrows():
    link = row.get("link")
    links.append(link)
    if not link or pd.isna(link):
        print(f"Row {index} has no valid PDF link. Skipping.")
        continue

    print(f"Processing row {index} with link: {link}")
    try:
        response = requests.get(link)
        if response.status_code == 200:
            # Save the PDF content into a temporary file
            pdf_filename = f"temp_{index}.pdf"
            with open(pdf_filename, "wb") as pdf_file:
                pdf_file.write(response.content)
            
            page_found = find_keyword_page_via_ocr(pdf_filename, KEYWORD, POPPLER_PATH)

            # Remove the temporary file
            os.remove(pdf_filename)
        else:
            print(f"Failed to download PDF for row {index}. HTTP status: {response.status_code}")
    except Exception as e:
        print(f"Error processing row {index}: {e}")

# Overwrites the original file
df['carbon_page'] = carbon_page
df['used_link'] = links
df.to_csv("filing_history.csv", index=False)
