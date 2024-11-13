import ocrmypdf
import pdfplumber
import os
import re

# Define file paths
input_pdf_path = "final-31-1-24-Annual-Report-2022-23-changes-2.pdf"  # Your input PDF file
ocr_pdf_path = "final_report_ocr.pdf"  # Output for OCR-processed PDF
output_folder = "outputs"
os.makedirs(output_folder, exist_ok=True)  # Create output folder if not exists

# Step 1: Perform OCR on the PDF using OCRmyPDF
print("Starting OCR processing...")
ocrmypdf.ocr(input_pdf_path, ocr_pdf_path, force_ocr=True, output_type="pdfa")
print("OCR processing completed.")

# Step 2: Extract text from the OCR-processed PDF and save it for inspection
text_output_path = os.path.join(output_folder, "extracted_text.txt")
with open(text_output_path, "w") as text_file:
    with pdfplumber.open(ocr_pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            text_file.write(f"--- Page {page_num} ---\n")
            text_file.write(text if text else "No text found on this page.\n")
            text_file.write("\n\n")

print(f"Extracted text saved to {text_output_path}")

# Step 3: Attempt to locate "Key Achievements" and associated data in the extracted text
key_achievements_data = []
section_found = False

# Regular expression to capture counts and descriptions (assuming patterns like "28,439 Individuals...")
pattern = re.compile(r"(\d{1,3}(?:,\d{3})*)\s+(.*)", re.IGNORECASE)

with pdfplumber.open(ocr_pdf_path) as pdf:
    for page_num, page in enumerate(pdf.pages, start=1):
        text = page.extract_text()
        
        # Check if "Key Achievements" section exists on this page
        if text and "Key Achievements" in text:
            print(f"Found 'Key Achievements' on page {page_num}")
            section_found = True

        if section_found:
            # Use regex to find counts and descriptions
            matches = pattern.findall(text)
            for match in matches:
                count, description = match
                key_achievements_data.append({
                    "Count": count,
                    "Description": description
                })

            # Stop after capturing data on the page with "Key Achievements"
            break

# Step 4: Save extracted data to CSV if found
if key_achievements_data:
    import pandas as pd
    df = pd.DataFrame(key_achievements_data)
    csv_path = os.path.join(output_folder, "key_achievements.csv")
    df.to_csv(csv_path, index=False)
    print(f"Key achievements data saved to {csv_path}")
else:
    print("No 'Key Achievements' data found in the PDF.")

print("Extraction completed.")
