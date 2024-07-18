import PyPDF2
import extract_vehicle_details
from extract_vehicle_details import vehicle_details
from datetime import datetime
import os
import re
import pandas as pd


def convert_to_float(value_str):
    try:
        # Check if the string contains commas
        if ',' in value_str:
            # Replace commas with an empty string to remove them
            value_str = value_str.replace(',', '')

        # Attempt to convert string to float
        return float(value_str)
    except ValueError:
        # Handle cases where conversion fails (e.g., non-numeric characters)
        return 0.0  # Return 0 if conversion fails or other errors occur

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text
def bajaj_two_wheeler_submodule(pdf_dir, output_excel):
    # List to store all extracted info
    all_info = []

    # Loop through all PDF files in the directory
    for filename in os.listdir(pdf_dir):
        if filename.endswith('.pdf'):
            pdf_text = extract_text_from_pdf(f'{pdf_dir}/{filename}')
            pdf_path = os.path.join(pdf_dir, filename)
            vehicle_info = extract_info(pdf_text,pdf_path)
            # for k ,v in vehicle_info.items():
            #     print(k+ ' - - '+ v)
            all_info.append(vehicle_info)
    return all_info
    # Convert the list of dictionaries to a DataFrame
    # df = pd.DataFrame(all_info)
    #
    # # Export the DataFrame to an Excel file
    # df.to_excel(output_excel, index=False)
    #
    # print(f"Data has been exported to {output_excel}")


def convert_date_format(date_str):
    # Define the input formats
    input_formats = ['%d-%b-%Y', '%b%Y', '%b/%Y', '%d-%m-%y','%d-%B-&Y','%B/%Y','%d-%B-%y','%B%Y','%d-%b-%y']
    # Define the output format
    output_format = '%Y/%m/%d'

    # Try parsing the input date string with each format
    for input_format in input_formats:

        try:
            date_obj = datetime.strptime(date_str, input_format)
            # Format the datetime object to the desired output format
            formatted_date = date_obj.strftime(output_format)
            return formatted_date
        except ValueError:
            # If parsing fails, try the next format
            continue

    # If all formats fail, return an error message or handle the error

    return 'Invalid date format'


# Function to extract information using regex
def extract_info(text,pdf_path):
    extracted_info = {}
    extract_vehicle_details.extract_veh_details(pdf_path)
    def extract_field(pattern, text,default = ' '):
        match = re.search(pattern, text)
        if match:
            if match.group(1):
                return match.group(1)
            elif match.group(2):
                return match.group(2)
        else:
            return default

    extracted_info['Policy Number'] = extract_field(r"policy number\s+'([A-Z0-9-]+)'", text)
    extracted_info["Insured Name"] = extract_field(r'Dear ([A-Za-z\s]+)[,\n]', text)
    extracted_info["Customer's Phone Number"] = extract_field(r'Proposer Mobile Number[:\s]+(\d+)', text)
    extracted_info["Customer's Email"] = extract_field(r'Proposer e-mail id[:\s]+([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', text)
    extracted_info["Insured Address"] = extract_field(r'Proposer Address\s*:\s*([^:]+?)\s*\d\.\s', text)
    extracted_info['Date of Issuance'] = extract_field(r'Policy [iI]ssued on\s+(\d{2}-[A-Za-z]{3}-\d{4})', text)
    try:
        extracted_info['Date of Issuance'] = convert_date_format(extracted_info['Date of Issuance'])
    except:
        print(f'Date of issuance incorrect format - {extracted_info['Date of Issuance']} in {pdf_path} - value : {extracted_info['Date of Issuance']}')
    extracted_info['Period of Insurance (From)'] = extract_field(r'From[\s:]+(\d{2}-[A-Za-z]{3,4}-\d{4})', text,' ')
    try:
        extracted_info['Period of Insurance (From)'] = convert_date_format(extracted_info['Period of Insurance (From)'])
    except:
        print(f'Period of Insurance (From) date incorrect format - {extracted_info['Period of Insurance (From)']} in {pdf_path} - value : {extracted_info['Period of Insurance (From)']}')
    extracted_info['Period of Insurance (To)'] = extract_field(r'To[\s:][\s:]+(\d{2}-[A-Za-z]{3,4}-\d{4})', text,' ')
    try:
        extracted_info['Period of Insurance (To)'] = convert_date_format(extracted_info['Period of Insurance (To)'])
    except:
        print(f'Period of Insurance (To) date incorrect format - {extracted_info['Period of Insurance (To)']} in {pdf_path} - value : {extracted_info['Period of Insurance (To)']}')
    extracted_info['Registration Number'] = extract_field(r'([A-Z]{2}\d{2}[A-Z]{1,3}\d{4})', text)
    extracted_info['RTO'] = extracted_info['Registration Number'][:4]
    extracted_info['NCB (%)'] = vehicle_details['NCB%']

    # Assuming vehicle_details is a dictionary available in the scope with the required fields
    extracted_info['Date of Registration'] = vehicle_details['Month/YearofRegn']
    try:
        extracted_info['Date of Registration'] = convert_date_format(extracted_info['Date of Registration'])
    except:
        print(f'Date of registration incorrect format - {extracted_info['Date of Registration']} in {pdf_path} - value : {extracted_info['Date of Registration']}')
    extracted_info['Make'] = vehicle_details['VehicleMake']
    extracted_info['Model'] = vehicle_details['VehicleModel']
    extracted_info['Variant'] = vehicle_details['VehicleSubType']
    extracted_info['Year of Manufacture'] = vehicle_details['YearofManufacture']
    extracted_info['Fuel Type'] = vehicle_details['FuelType']
    extracted_info['Engine Number'] = vehicle_details['EngineNumber']
    extracted_info['Chassis Number'] = vehicle_details['ChassisNumber']
    extracted_info['Seating Capacity'] = vehicle_details['SeatingCapacity']
    extracted_info['CC'] = vehicle_details['CubicCapacity/Kilowatt']
    extracted_info['Previous Insurer Name'] = extract_field(r'\(i\) Insurance Provider[:\s]+([\w\s]+)|Previous Insurer\s*-\s*([^\n.]+)[.Previous]', text)

    extracted_info['Previous Insurer Name'] = ' ' if extracted_info['Previous Insurer Name'] == 'NA\n' or extracted_info['Previous Insurer Name'] == 'NA' else extracted_info['Previous Insurer Name']

    extracted_info['Previous Policy No'] = extract_field( r'Previous Policy No\s*[-:]\s*([A-Za-z0-9/]+)',text)
    extracted_info['Previous Policy No'] = ' ' if extracted_info['Previous Policy No'] == 'NA' else extracted_info['Previous Policy No']
    extracted_info['Previous Policy Expiry Date'] = extract_field(r'Expiry On\s*-\s*(\d{2}-[A-Z]{3}-\d{2})|Previous Policy Expiry Date\s*:\s*(\d{2}-[A-Z]{3}-\d{2})',text)
    if extracted_info['Previous Policy Expiry Date'] != ' ':
        try:
            extracted_info['Previous Policy Expiry Date'] = convert_date_format(extracted_info['Previous Policy Expiry Date'])
        except:
            print(f'Previous Policy Expiry date incorrect format - {extracted_info['Previous Policy Expiry Date']} in {pdf_path} - value : {extracted_info['Previous Policy Expiry Date']}')
    # extracted_info['Total IDV'] = extract_field(r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s+C\. Coverage opted',text,0)
    extracted_info['Total IDV'] = vehicle_details['TotalIDV(inRs.)']
    extracted_info['Total OD Premium (A)'] = extract_field(r'Total OD Premium - A[\s]+(\b\d{1,3}(?:,\d{2})*\.\d{2}\b)|Total Own Damage Premium:[\s]*(\b\d{1,3}(?:,\d{3})*\.\d{2}\b)',text,'0')
    extracted_info['Third Party Liability (B)'] = extract_field( r'Total Liability Premium[:\s]*(\b\d{1,3}(?:,\d{3})*\.\d{2}\b)|Total Act Premium - B[\s]*(\b\d{1,3}(?:,\d{3})*\.\d{2}\b)',text,'0')
    # extracted_info['Net Premium(A+B)'] = extract_field(r'Net Premium[\s]*()(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',text,0)
    extracted_info['Net Premium(A+B)'] = convert_to_float(extracted_info['Total OD Premium (A)']) + convert_to_float(extracted_info['Third Party Liability (B)'])
    sgst = extract_field(r'State GST \(9%\)[\s]*(\b\d{1,3}(?:,\d{2})*\.\d{2}\b)',text)

    sgst = convert_to_float(sgst)

    cgst = extract_field(r'Central GST \(9%\)[\s]*(\b\d{1,3}(?:,\d{2})*\.\d{2}\b)',text)

    cgst = convert_to_float(cgst)


    igst = extract_field(r'Integrated GST \(18%\)\s*(\d{1,3}(?:,\d{3})*\.\d{2})',text)

    igst = convert_to_float(igst)

    extracted_info['GST'] = (sgst+cgst+igst)
    # extracted_info['Final Premium'] = extract_field(r'Final Premium Rs.[\s]+(\d{1,3}(?:,\d{3})*\.\d{2})',text)
    extracted_info['Final Premium'] = extracted_info['Net Premium(A+B)'] + extracted_info['GST']
    return extracted_info
def export_to_xlsx(folder_path, output_excel_path):
    all_details = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            pdf_text = extract_text_from_pdf(pdf_path)
            extract_vehicle_details.extract_veh_details(pdf_path)
            details = extract_info(pdf_text)
            all_details.append(details)

    df = pd.DataFrame(all_details)
    df.to_excel(output_excel_path, index=False)

# pdf_path = 'Bajaj Insurances/OG-25-1901-1806-00024047.pdf'

# pdf_text = extract_text_from_pdf(pdf_path)
# print(pdf_text)
# info = extract_info(pdf_text)

# for key, value in info.items():
#     print(f'{key}: {value}')
#


# Directory containing the PDFs
# pdf_dir = 'Insurance_pdf/Bajaj 2 wheeler Insurances'
#
# output_excel = 'Extraction_Bajaj_Excel/extracted_bajaj_2wheeler_info.xlsx'
#
# # Call the function to convert PDF information to Excel
# convert_to_excel(pdf_dir, output_excel)