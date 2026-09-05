import pandas as pd
from dotenv import load_dotenv

from src.data.drive_bot import DriveBot
from src.data.transform_dataframe import transform_dataframe
from src.data.aniversariantes import aniversariantes_do_dia
from src.notifications.email_aniversariantes import enviar_email_aniversariantes

load_dotenv()

drive_bot = DriveBot()
dataframe = transform_dataframe(drive_bot.get_data())
hoje = pd.Timestamp.now()

hoje_df = aniversariantes_do_dia(dataframe)
enviar_email_aniversariantes(hoje_df, hoje)