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
        data = worksheet.get_all_values()
        dataframe = pd.DataFrame(data[1:], columns=data[0])
        return dataframe