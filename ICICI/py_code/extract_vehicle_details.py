
import pdfplumber
vehicle_details = {}
def extract_tabledata_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        all_tables = []
        # Iterate over pages starting from the second page
        for page_number in range(1, len(pdf.pages)):
            page = pdf.pages[page_number]
            tables = page.extract_tables()
            for table in tables:
                all_tables.extend(table)
    convert_to_dict(all_tables)

def convert_to_dict(all_tables):
    for i in range(len(all_tables)-2):
      if len(all_tables[i]) == len(all_tables[i+1]):
        for j in range(len(all_tables[i])):
          if all_tables[i][j] != None and all_tables[i+1][j] != None:
            vehicle_details[all_tables[i][j]] = all_tables[i+1][j]



pdf_path = r"C:\Users\Abhinav nair\PycharmProjects\Insurance pdf reader\ICICI\ICICI insurance pdfs\ICICI 2 wheeler insurances\3005A35225130900B00.pdf"
tables = extract_tabledata_from_pdf(pdf_path)
cleaned_vehicle_details = {}
for k, v in vehicle_details.items():
    # Clean the key
    cleaned_key = k.replace('\n', ' ').replace('.', '')
    # Add to the new dictionary
    cleaned_vehicle_details[cleaned_key] = v

# Print the cleaned dictionary
for k, v in cleaned_vehicle_details.items():
    print(f"{k} -- {v}")
