from Bajaj.py_code.bajaj_two_wheeler import convert_date_format
table_details = {}

def extract_table_details(text):
    # Locate the start position of "Engine No."
    period_insurance_no_pos = text.find("Period of Insurance")
    if period_insurance_no_pos == -1:
        return "Period of Insurance"

    # Extract the substring starting from the position after "Engine No."
    policy_from_and_to_date = text[period_insurance_no_pos:].split('\n')[8].strip()
    policy_start,policy_end = extract_policy_dates(policy_from_and_to_date)
    table_details["policy_start"] = convert_date_format(policy_start)
    table_details["policy_end"] = convert_date_format(policy_end)

    vehicle_make_model = text[period_insurance_no_pos:].split('\n')[9].strip()
    veh_make,veh_model = extract_make_and_model(vehicle_make_model)
    table_details["vehicle_make"] = veh_make
    table_details["vehicle_model"] = veh_model

    veh_registration_num = text[period_insurance_no_pos:].split('\n')[11].strip()
    table_details["veh_reg_num"] = veh_registration_num

    cc_pos = text.find("CC/KW")
    if cc_pos != -1:
        # Extract the CC value
        cc_value = text[cc_pos:].split('\n')[12].strip()
    else:
        cc_value = 0
    table_details["cc"] = cc_value

    mfg_year = text[cc_pos:].split('\n')[13].strip()
    table_details["mfg_year"] = mfg_year

    seating_cap = text[cc_pos:].split('\n')[14].strip()
    table_details["seating_cap"] = seating_cap

    chassis = text[cc_pos:].split('\n')[15].strip()
    table_details["chassis"] = chassis

    engine_num = text[cc_pos:].split('\n')[16].strip()
    table_details["engine_num"] = engine_num





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
text = '''
eference No. W332447600
Date: Jul 17, 2024
BHOJA BHAI  BHARWAD
BHARWAR CHAWL  OPP  ADARSH MANDAL
RAWAL PADA
MUMBAI
MAHARASHTRA 400068
Mobile No: 9004863245
 
Sub: Risk Assumption Letter
 
Dear BHOJA BHAI  BHARWAD,
 
We value your relationship with ICICI Lombard General Insurance Company Limited and thank you for choosing us as your preferred insurance provider.
 
Please find enclosed Policy No. 3005/A/352251309/00/B00 , The same has been issued based on below mentioned details, provided by you at the time of policy 
purchase.
 
Insured & Vehicle Details
Name of the Insured
Period of Insurance
Vehicle Make / Model
RTO City
Vehicle Registration No.
Vehicle Registration Date
Engine No.
Chassis No.BHOJA BHAI  BHARWAD
Jul 18, 2024 to Jul 17, 2025
HONDA MOTORCYCLE / ACTIVA 3G
MAHARASHTRA-MUMBAI
MH47F4812
Sep 30, 2015
JF50ET2695901
ME4JF504HFT695562
Previous Policy Details
Previous Policy No.
Previous Policy Period
Claims Made Under Previous Policy
Previous Insurer Name
Previous Policy Type2333444444
Jul 07, 2023 to Jul 06, 2024
0
GODIGIT
TP
1
Thecommencement ofcoverage ofriskunder thepolicy issubject torealisation ofpayment ofpremium infull.Incase thepremium isnotrealised dueto
cheque dishonour or any other reason, the insurance cover shall be void ab-initio.
1
We have issued the policy basis your confirmation that you hold a valid PUC and/or Fitness certificate, as applicable.
1Government ofIndia hasmandated electronic tollpayments using FASTag toreduce vehicular traffic attollplazas. Customers areadvised tocomply withthe
direction ofthegovernment andgettheir FASTag from Point ofSale locations atTollPlazas orfrom Issuer Agency. Please visit http://www.fastag.org/ for
details.
“Updating your bank details withuswould helpfacilitating future transactions. Bank details canbeeasily updated using “IL–Take care”App.Download theapp
now for all your insurance and wellness needs and for faster resolution”
Please check thepolicy details foraccuracy. Should youfindanydiscrepancy /require anychanges intheCertificate ofInsurance cum Policy Schedule, please
contact usimmediately atourtollfreenumber 1800 2666 oremail usatcustomersupport@icicilombard.com, sothatwecanrectify thesame. Absence ofany
communication within a period of 15 days of the date mentioned on this letter, would mean that the issued policy is in order and as per your proposal.
Important Points:
a. Any accidental loss, damage and/or liability caused, sustained or incurred, while vehicle not being registered permanently will not be covered.
b.Anyminor scratches tothevehcile, paint fading, wear andteararising outofnormal useandrequiring touch-up orminor repair under routine maintenance will
not be covered.
c.Anyliability ofwhatsoever nature caused by,contributed byorarising duetothevehicle being driven byaperson without having valid driving license willnotbe
covered.
( Please visist www.icicilombard.com for the policy wordings, for complete details on terms and conditions governing the coverage and NCB)
Theinformation provided ismerely illustrative andshall notbeconstrued tobeanevidence ofexistence ofacontract ofinsurance. TheRisk Assumption Letter
is to be read in conjunction with the policy and shall be considered null and void without the same.
TheCompulsory Personal Accident cover hasnotbeen opted inthispolicy onaccount that,theOwner driver hasaseparate existing Personal Accident cover
against Death and Permanent Disability (Total and Partial) for Sum Insured of at least Rs.15 lacs.1
1
Product Code: 3005/A   UIN: IRDAN115RP0016V01200102
 CORP/SUP/OPI/2014/1777        Jul 17, 2024Name of the Insured :BHOJA BHAI  BHARWAD Policy No. :3005/A/352251309/00/B00
Address :BHARWAR CHAWL  OPP  ADARSH MANDAL RAWAL PADA
DAHISAR EAST,     MUMBAI, MAHARASHTRA 400068Period of Insurance :Jul 18, 2024 12:00 to
Midnight of Jul 17, 2025
Telephone No : Mobile No: 9004863245 E-Policy No. :ESB-638568315183071999
Email Address :SP77@GMAIL.COM Policy Issued On :Jul 17, 2024
Nominee Name :Vijay Named Passenger's Nominee: Covernote No. :352251309
Relationship :Son - RTO Location :MAHARASHTRA-MUMBAI
Age : - Hypothecated To :-
GSTIN No. (Customer) : Invoice No. :1007241521747
Servicing Branch Name :Mumbai
Servicing Branch Address :414, ICICI LOMBARD HOUSE, VEER SAVARKAR MARG, NEAR SIDDHI VINAYAK TEMPLE MAIN GATE, PRABHADEVI, MUMBAI,
400025, MAHARASHTRA
Politically Exposed Person (PEP)/close relative of PEP: No
Vehicle Registration
NoMake Model Type of Body CC/KW Mfg Yr Seating
CapacityChassis No. Engine No.
MH47F4812HONDA
MOTORCYCLEACTIVA 3G  Solo With
Pillion109 2015 2 ME4JF504HFT695562 JF50ET2695901
  Premium Details
LIABILITY (`)
Basic Third Party Liability  
Total  714.00  
714.00  
 
Total Liability Premium 714.00
CGST% 9.00
` 64.26
SGST% 9.00
` 64.26
UTGST% 0.00
` 0.00
IGST% 0.00
` 0.00
Total Tax Payable in ` 129.00
Total Premium Payable In ` 843.00
Geographical Area: India Applicable IMT Clauses: 
Premium Collection No. 1211958466 Premium Amount ( `) ` 843.00 Receipt Date Jul 17, 2024
GSTIN Reg.No 27AAACI7904G1ZN HSN/SAC code 997134 / GENERAL INSURANCE SERVICES   
We hereby declare that though our aggregate turnover in any preceding financial year from 2017-18 onwards is more than the aggregate turnover notified under sub-rule (4) of
rule 48, we are not required to prepare an invoice in terms of the provisions of the said sub-rule.
Limits ofLiability: (a)Under Section II-I(i) of the policy: Death of or bodily injury & (b) Under Section II-I(ii) of the policy: Damage to Third Party Property- Such amount as is 
necessary tomeet therequirements oftheMotor Vehicles (Amendment) Act, 2019 ;PACover forOwner-Driver under Section III:CSI 0.00/-. The Compulsory Personal 
Accident cover has notbeen opted inthis policy onaccount that, theOwner driver has aseparate existing Personal Accident cover against Death and Permanent 
Disability (Total and Partial) forSum Insured of at least Rs.15 lacs. Limitations as to Use:  The Policy covers use of the vehicle for any purpose other than: Hire or Reward, 
carriage ofgoods (other than samples orpersonal luggage), Organized racing, Pace making, Speed testing, Reliability trials, any purpose in connection with Motor trade.  
Driver's Clause: Any person including the insured: Provided that a person driving holds an effective driving license at the time of the accident and is not disqualified from 
holding orobtaining such alicense. Provided also that theperson holding aneffective learner's license may also drive the vehicle and that such a person satisfies the 
requirements ofRule 3oftheCentral Motor Vehicles Rules, 1989. Important Notice: The insured isnotindemnified ifthevehicle isused ordriven otherwise than in 
accordance with this schedule. Any payment made bytheCompany byreason ofwider terms appearing in the Certificate in order to comply with the Motor Vehicle Act, 
1988 is recoverable from the insured. See the clause headed "AVOIDANCE OF CERTAIN TERMS AND RIGHT OF RECOVERY".  
Inconsideration ofthe premium for this extension being calculated at a pro-rata proportion of the annual premium, it is hereby declared and agreed by the insured that upon 
expiry ofthis extension, this policy shall be renewed for a period of twelve months, failing which the difference between the extension premium now paid on pro rata basis 
and the premium at short period rate shall become payable by the insured.  
ForLegal interpretation, English version will hold good. Disclaimer: Please visit www.icicilombard.com forthepolicy wordings, forcomplete details onterms and 
conditions governing the coverage and NCB. This document is to be read with the policy wordings. The policy is valid subject to realization of cheque. We accept premium 
only via legally recognized modes. In case of dishonour of premium cheque, the company shall not be liable under the policy and the policy shall be void ab-initio. In case 
ofany discrepancy with respect to the policy, please revert within 15 days from the policy start date. This policy is underwritten on the basis of the information provided by 
you and asdetailed inthe Risk Assumption Letter shared with you along with the policy. On renewal, the benefits provided under the policy and/or terms and conditions of 
thepolicy including premium rate may besubject tochange. Grievance Redressal:  For resolution of any query or grievance you may contact us on our toll free no. 1800 
2666, orvisit any ofourbranch offices. You can also write tousatcustomersupport@icicilombard.com. Fordetailed grievance redressal mechanism please visit the 
"Grievance Redressal" section on our website www.icicilombard.com.  
The Company reserves the right tocancel this Policy immediately upon becoming aware ofany mis-representation, fraud, non-disclosure ofmaterial facts or 
non-cooperation by or on behalf of the Insured; the Company is not obliged to refund the premium paid under this Policy  
I/We hereby certify that thePolicy towhich this Certificate relates, as well as, this Certificate of Insurance are issued in accordance with the provisions of Chapter X and 
Chapter XI of M.V. Act, 1988. In witness whereof, this Policy has been signed at Mumbai on this date of Jul 17, 2024 in lieu of Covernote No. 352251309. The stamp duty of 
` 0.50 paid vide deface no. CSD0220242018 dated Apr 10, 2024.  
Policy Issuing Office: ICICI Lombard General Insurance Company Limited, ICICI LOMBARD HOUSE, 414, Veer Savarkar Marg, Near Siddhi Vinayak Temple, Prabhadevi, 
Mumbai 400 025.  
Warranted that theinsured named herein/owner ofthevehicle holds a valid Pollution Under Control (PUC) Certificate and/or valid fitness certificate, as applicable, on the 
date ofcommencement ofthePolicy and undertakes torenew and maintain a valid and effective PUC and/or fitness Certificate, as applicable, during the subsistence of 
the Policy. Further, the Company reserves the right to take appropriate action in case of any discrepancy in the PUC or fitness certificate.1 CERTIFICATE OF INSURANCE CUM POLICY SCHEDULE
Two Wheeler Vehicles Liability Policy1
Product Code: 3005/A   UIN: IRDAN115RP0016V01200102
 CORP/SUP/OPI/2014/1777        Jul 17, 2024Point of Sale (POS) Details
POS Number POS Name Contact Details PAN Card Number
201943350997 SANJAY S PASWAN 7304332968 AACCP8264G
Agency Code:DB10603
Agency Name:PROBUS INSURANCE BROKER
PRIVATE LIMITED
Agent's Contact No:8976982994
Contact Person: 
1 CERTIFICATE OF INSURANCE CUM POLICY SCHEDULE
Two Wheeler Vehicles Liability Policy1
Product Code: 3005/A   UIN: IRDAN115RP0016V01200102
 CORP/SUP/OPI/2014/1777        Jul 17, 2024'''
extract_table_details(text)