import os
import re
import pandas as pd
from PyPDF2 import PdfReader

from Bajaj.py_code.Bajaj_pcv import bajaj_pcv_submodule
from Bajaj.py_code.bajaj_gcv import bajaj_gcv_submodule
from Bajaj.py_code.bajaj_private_car import bajaj_private_car_submodule
from Bajaj.py_code.bajaj_two_wheeler import bajaj_two_wheeler_submodule


# 'Insurance_pdf\\Bajaj gcv and pcv insurances\\OG-19-1901-1803-00005678.pdf'
# Bajaj/Insurance_pdf/Bajaj gcv and pcv insurances/OG-19-1901-1803-00005678.pdf
def main():
    base_dir = "../Insurance_pdf"
    output_excel = "Extracted_Bajaj_Excel/bajaj_output.xlsx"
    combined_data = []

    for Bajaj_sub_module_dir in ["Bajaj 2 wheeler Insurances",
                                 "Bajaj gcv and pcv insurances", "Bajaj private car insurances"]:
        sub_module_path = os.path.join(base_dir, Bajaj_sub_module_dir)
        for pdf_file in os.listdir(sub_module_path):
            pdf_path = os.path.join(sub_module_path, pdf_file)
            submodule_name = detect_submodule(pdf_path)
            if submodule_name == "GCV":
                details = bajaj_gcv_submodule(pdf_path)
                combined_data.extend(details)
            elif submodule_name == "Private Car":
                details = bajaj_private_car_submodule(pdf_path)
                combined_data.extend(details)
            elif submodule_name == "Two-Wheeler":
                details = bajaj_two_wheeler_submodule(pdf_path)
                combined_data.extend(details)
            elif submodule_name == "PCV":
                details = bajaj_pcv_submodule(pdf_path)
                combined_data.extend(details)
            else:
                print(f'No match for {pdf_file}')

            # Handle other companies as needed

    # Create a DataFrame from combined_data

    df = pd.DataFrame(combined_data)

    # Export the DataFrame to an Excel file
    df.to_excel(output_excel, index=False)


def detect_submodule(pdf_path):
    pcv_pattern = r'(Passenger Carrying)'
    car_pattern = r'Private\s*Car|PrivateCar'
    twoWheeler_pattern = r'(Two[-\s]?Wheeler)'

    gcv_pattern = r'(Goods Carrying)'

    # Function to detect company name from first page of PDF
    with open(pdf_path, 'rb') as f:
        reader = PdfReader(f)
        page_text = reader.pages[0].extract_text()
        page_text += reader.pages[2].extract_text()

        match = re.search(twoWheeler_pattern, page_text, re.IGNORECASE)
        if match:
            print(f"Match found: {match.group()}")
            return "Two-Wheeler"
        match = re.search(pcv_pattern, page_text, re.IGNORECASE)
        if match:
            print(f"Match found: {match.group()}")
            return "PCV"
        match = re.search(gcv_pattern, page_text, re.IGNORECASE)
        if match:
            print(f"Match found: {match.group()}")
            return "GCV"
        match = re.search(car_pattern, page_text, re.IGNORECASE)
        if match:
            print(f"Match found: {match.group()}")
            return "Private Car"
        return 'None'


if __name__ == "__main__":
    main()
