import pdfplumber
def strip_whitespaces(all_tables):

    new_table = []
    for row_val in all_tables:
        new_row_val = []
        for cell_val in row_val:
            new_cell_val = []
            for text in cell_val:
                new_text =''
                new_text = text.replace('\n','')
                new_text = new_text.replace('-','')
                new_cell_val.append(new_text)
            new_row_val.append(new_cell_val)
            new_table.append(new_row_val)
    new_table = new_table[:3]
    return new_table


vehicle_details = {}
def convert_to_dict(cleaned_table):
    temperory_dict = {cleaned_table[0][i]: cleaned_table[1][i] for i in range(len(cleaned_table[0]))}
    vehicle_details.update(temperory_dict)

    # print(vehicle_details)


def extract_veh_details(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        veh_details = {}
        all_tables = []
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                all_tables.append(table)
    cleaned_tables = strip_whitespaces(all_tables[:3])
    for cleaned_table in cleaned_tables:
        convert_to_dict(cleaned_table)

    # Example usage


# pdf_path = "Bajaj Insurances/OG-25-1901-1806-00024045.pdf"
# tables = extract_veh_details(pdf_path)
# print(type(tables))
# print(vehicle_details)
# # for row in tables:
# #     print(row)