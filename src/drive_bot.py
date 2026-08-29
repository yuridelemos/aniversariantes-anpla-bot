import json
import os
import pandas as pd

from dotenv import load_dotenv
import gspread

load_dotenv()
SHEET = os.getenv("SHEET_LINK")

class DriveBot:
    def __init__(self):
        self.gc = gspread.service_account(filename="credentials.json")

    def get_data(self):
        sh = self.gc.open_by_key(SHEET)
        worksheet = sh.sheet1
        dataframe = pd.DataFrame(worksheet.get_all_values())
        return dataframe