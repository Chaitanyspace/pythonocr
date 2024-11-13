import streamlit as st
import re

def load_text():
    # Load the extracted OCR text with fallback for encoding errors
    try:
        with open("outputs/extracted_text.txt", "r", encoding="utf-8") as file:
            text = file.read()
    except UnicodeDecodeError:
        with open("outputs/extracted_text.txt", "r", encoding="latin1") as file:
            text = file.read()
    return text

def parse_key_achievements(text):
    achievements_data = []

    # Split the content by pages
    achievements_sections = re.split(r'--- Page \d+ ---', text)

    for section in achievements_sections:
        # Look for "Key" and "Achievements" across two lines
        if 'Key' in section and 'Achievements' in section.splitlines()[1:3]:
            capturing = False
            section_data = []

            # Process the section line-by-line
            lines = section.splitlines()
            for i, line in enumerate(lines):
                # Start capturing if "Key Achievements" pattern is found
                if line.strip() == "Key" and i+1 < len(lines) and lines[i+1].strip() == "Achievements":
                    capturing = True
                    continue  # Skip "Key Achievements" header

                if capturing:
                    # Stop capturing on encountering a new section or empty line
                    if not line.strip() or "---" in line:
                        break

                    # Match numbers followed by descriptions
                    match = re.findall(r'(\d{1,3}(?:,\d{3})*|\d+)\s+(.*)', line.strip())
                    if match:
                        for count, description in match:
                            section_data.append({"Count": count, "Description": description})
                    else:
                        # Check if this line is a continuation of a previous description
                        if section_data and line.strip():
                            section_data[-1]["Description"] += " " + line.strip()

            # Add parsed data for this section
            if section_data:
                achievements_data.extend(section_data)

    return achievements_data

def main():
    # Streamlit app setup
    st.title("Plan India PDF Report Parser")
    st.write("This app extracts 'Key Achievements' from the report and displays them in a tabular format.")

    # Load and display extracted text
    text = load_text()

    # Parse 'Key Achievements' data
    achievements = parse_key_achievements(text)

    # Display results
    st.header("Key Achievements from the PDF Report")
    if achievements:
        st.table(achievements)
    else:
        st.write("No achievements data found for this section.")

if __name__ == "__main__":
    main()
