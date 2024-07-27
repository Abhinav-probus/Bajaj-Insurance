from Bajaj.py_code.bajaj_two_wheeler import convert_date_format
table_details = {}

def extract_prev_policy_details(text):
    # Locate the start position of "Engine No."
    prev_policy_no_pos = text.find("Previous Policy Details")
    if prev_policy_no_pos == -1:
        return prev_policy_no_pos

    prev_policy_no  = text[prev_policy_no_pos :].split('\n')[7].strip()
    # veh_make,veh_model = extract_make_and_model(vehicle_registration)
    table_details["policy number"] = prev_policy_no

    prev_policy_duration = text[prev_policy_no_pos:].split('\n')[8].strip()
    try:
        policy_end_date = prev_policy_duration.split(' to ')[1]
        policy_end_date = convert_date_format(policy_end_date)
    except:
        policy_end_date = ' '
        print(f"policy end date error")
    table_details["Policy end date"] = policy_end_date

    ncb = text[prev_policy_no_pos:].split('\n')[9].strip()
    table_details["NCB"] = ncb[:-1]

    previous_insurer = text[prev_policy_no_pos:].split('\n')[11].strip()
    table_details["Previous insurer name"] = previous_insurer






def extract_make_and_model(text):
    # Split the text using " / " as the delimiter
    parts = text.split(" / ")
    if len(parts) != 2:
        return "Invalid format", None

    # Extract and return the make and model
    make = parts[0].strip()
    model = parts[1].strip()
    return make, model

def extract_policy_dates(text):
    # Split the text using " to " as the delimiter
    dates = text.split(" to ")
    if len(dates) != 2:
        return "Invalid date format", None

    # Extract and return the from date and to date
    from_date = dates[0].strip()
    to_date = dates[1].strip()
    return from_date, to_date
