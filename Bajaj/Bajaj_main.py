import PyPDF2
import extract_vehicle_details
from extract_vehicle_details import vehicle_details
from datetime import datetime
import os
import re
import pandas as pd


def extract_subtype_from_firstpage(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        page = pdf_reader.pages[0]
        text += page.extract_text()
    return text
