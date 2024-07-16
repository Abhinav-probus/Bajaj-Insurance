import PyPDF2
import extract_vehicle_details
from extract_vehicle_details import vehicle_details
import openpyxl
import os
import re
import pandas as pd
import pdfplumber
'''
I am unable to extract the values for vehicle details . Therefore I have plan to use pdfplumber . Which extracts the 
the table values from the pdf and stores them in list of lists . But I have some issue regarding the code. The issues I will sort out later
and will focus on another company pdf.
'''
def export_to_xlsx(folder_path, output_excel_path):
    all_details = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            pdf_text = extract_text_from_pdf(pdf_path)
            details = extract_info(pdf_text)
            all_details.append(details)

    df = pd.DataFrame(all_details)
    df.to_excel(output_excel_path, index=False)



def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

# Function to extract information using regex
def extract_info(text):
    extracted_info = {}

    def extract_field(pattern, text):
        match = re.search(pattern, text)
        if match:
            if match.group(1):
                return match.group(1)
            elif match.group(2):
                return match.group(2)
        else:
            return ' '

    extracted_info['Policy Number'] = extract_field(r"policy number\s+'([A-Z0-9-]+)'", text)
    extracted_info["Insured Name"] = extract_field(r'Dear ([A-Za-z\s]+)[,\n]', text)
    extracted_info["Customer's Phone Number"] = extract_field(r'Proposer Mobile Number[:\s]+(\d+)', text)
    extracted_info["Customer's Email"] = extract_field(r'Proposer e-mail id[:\s]+(\w+@\w+\.\w+)', text)
    extracted_info["Insured Address"] = extract_field(r'Proposer Address\s*:\s*([^:]+?)\s*\d\.\s', text)
    extracted_info['Date of Issuance'] = extract_field(r'Policy Issued on[:\s](\d{2}-[A-Za-z]{3,4}-\d{4})\b', text)
    extracted_info['Period of Insurance (From)'] = extract_field(r'From[\s:]+(\d{2}-[A-Za-z]{3,4}-\d{4})', text)
    extracted_info['Period of Insurance (To)'] = extract_field(r'To[\s:][\s:]+(\d{2}-[A-Za-z]{3,4}-\d{4})', text)
    extracted_info['Registration Number'] = extract_field(r'([A-Z]{2}\d{2}[A-Z]{1,3}\d{4})', text)
    extracted_info['RTO'] = extracted_info['Registration Number'][:4]

    # Assuming vehicle_details is a dictionary available in the scope with the required fields
    extracted_info['Make'] = vehicle_details['VehicleMake']
    extracted_info['Date of Registration'] = vehicle_details['Month/YearofRegn']
    extracted_info['Model'] = vehicle_details['VehicleModel']
    extracted_info['Variant'] = vehicle_details['VehicleSubType']
    extracted_info['Year of Manufacture'] = vehicle_details['YearofManufacture']
    extracted_info['Fuel Type'] = vehicle_details['FuelType']
    extracted_info['Engine Number'] = vehicle_details['EngineNumber']
    extracted_info['Chassis Number'] = vehicle_details['ChassisNumber']
    extracted_info['Seating Capacity'] = vehicle_details['SeatingCapacity']
    extracted_info['CC'] = vehicle_details['CubicCapacity/Kilowatt']
    extracted_info['Previous Insurer Name'] = extract_field(r'\(i\) Insurance Provider[:\s]+([\w\s]+)|Previous Insurer[-\s]*([\w\s]+)\s*Previous Policy No', text)
    extracted_info['Previous Policy No'] = extract_field( r'Previous Policy No[-:\s]*\s*([\w]+)[,\s]',text)
    extracted_info['Expiring Policy Expiry Date'] = extract_field(r'Previous Policy Expiry Date\s*:\s*(\d{2}-[A-Z]{3,4}-\d{2})',text)
    extracted_info['Total IDV'] = extract_field(r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s+C\. Coverage opted',text)
    extracted_info['Total OD Premium (A)'] = extract_field(r'Own Damage Premium[\s]+(\b\d{1,3}(?:,\d{2})*\.\d{2}\b)|Total premium[\s]+(\b\d{1,3}(?:,\d{3})*\.\d{2}\b)',text)
    extracted_info['Third Party Liability (B)'] = extract_field( r'Third Party Liability[\s]+(\b\d{1,3}(?:,\d{3})*\.\d{2}\b)',text)
    extracted_info['Net Premium(A+B)'] = float(extracted_info['Total OD Premium (A)'])+ float(extracted_info['Third Party Liability (B)'])
    sgst = extract_field(r'State GST \(9%\)[\s]*(\b\d{1,3}(?:,\d{2})*\.\d{2}\b)',text)
    if sgst.isdigit():
        sgst = float(sgst)
    else:
        sgst = 0
    cgst = extract_field(r'Central GST \(9%\)[\s]*(\b\d{1,3}(?:,\d{2})*\.\d{2}\b)',text)
    if cgst.isdigit():
        cgst = float(cgst)
    else:
        cgst = 0


    igst = extract_field(r'Integrated GST \(18%\)[\s]*(\b\d{1,3}(?:,\d{2})*\.\d{2}\b)',text)
    if igst.isdigit():
        igst = float(igst)
    else:
        igst = 0
    extracted_info['GST'] = sgst+cgst+igst
    extracted_info['Final Premium'] = extracted_info['Net Premium(A+B)'] + extracted_info['GST']
    return extracted_info

pdf_path = 'Bajaj Insurances/OG-25-1901-1806-00024041.pdf'
extract_vehicle_details = extract_vehicle_details.extract_veh_details(pdf_path)
pdf_text = extract_text_from_pdf(pdf_path)
# print(pdf_text)
info = extract_info(pdf_text)
for key, value in info.items():
    print(f'{key}: {value}')
# Test with a folder path containing PDFs
folder_path = 'Bajaj Insurances'  # Update with your folder path
output_excel_path = 'Extraction_Bajaj_Excel/Extraction_Test.xlsx'  # Update with your desired output Excel file path

export_to_xlsx(folder_path, output_excel_path)

