import os
import re
import pandas as pd
from PyPDF2 import PdfReader

from Bajaj.bajaj_private_car import bajaj_private_car_submodule
from Bajaj.bajaj_two_wheeler import bajaj_two_wheeler_submodule
from Bajaj.bajaj_pcv_gcv import bajaj_pcv_and_gcv_submodule


def main():
    base_dir = "Insurance_pdf"
    output_excel = "output.xlsx"
    combined_data = []

    for Bajaj_sub_module_dir in ["Bajaj gcv and pcv insurances", "Bajaj private car insurances", "Bajaj 2 wheeler Insurances"]:
        sub_module_path = os.path.join(base_dir, Bajaj_sub_module_dir)
        for pdf_file in os.listdir(sub_module_path):
            pdf_path = os.path.join(sub_module_path, pdf_file)
            submodule_name = detect_submodule(pdf_path)
            if submodule_name == "Commercial":
                details = bajaj_pcv_and_gcv_submodule(pdf_path)
                combined_data.extend(details)
            elif submodule_name == "Private Car":
                details = bajaj_private_car_submodule(pdf_path)
                combined_data.extend(details)
            elif submodule_name == "Two-Wheeler":
                details = bajaj_two_wheeler_submodule(pdf_path)
                combined_data.extend(details)
            # Handle other companies as needed

    # Create a DataFrame from combined_data

    df = pd.DataFrame(combined_data)

    # Export the DataFrame to an Excel file
    df.to_excel(output_excel, index=False)


def detect_submodule(pdf_path):
    pattern1 = r'\b\w*commercial\w*\b'
    pattern2 = r'\b\w*private car\w*\b'
    pattern3 = r'\b\w*two-wheeler\w*\b'

    # Function to detect company name from first page of PDF
    with open(pdf_path, 'rb') as f:
        reader = PdfReader(f)
        first_page_text = reader.pages[0].extract_text().lower()
        if re.search(pattern1,reader):
            return "Commercial"
        elif "Private Car" in first_page_text.lower():
            return "Private Car"
        elif "Two-Wheeler" in first_page_text.lower():
            return "Two-Wheeler"
        # Add more conditions for other companies
        else:
            return None

if __name__ == "__main__":
    main()
