import json
import os
import pandas as pd
from dotenv import load_dotenv
import gspread

load_dotenv()
SHEET = os.getenv("SHEET_LINK")
if not SHEET:
    raise RuntimeError("Variável de ambiente SHEET_LINK não foi definida.")

def _garantir_credentials_json():
    """Se o arquivo não existir localmente, recria a partir da variável de ambiente."""
    if os.path.exists("credentials.json"):
        return
    conteudo = os.getenv("GOOGLE_CREDENTIALS_JSON")
    if conteudo:
        with open("credentials.json", "w") as f:
            f.write(conteudo)


class DriveBot:
    def __init__(self):
        _garantir_credentials_json()
        self.gc = gspread.service_account(filename="credentials.json")

    def get_data(self):
        sh = self.gc.open_by_key(SHEET)
        worksheet = sh.sheet1
        data = worksheet.get_all_values()
        dataframe = pd.DataFrame(data[1:], columns=data[0])
        return dataframe