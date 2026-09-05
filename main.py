from src.telegram_bot import TelegramBot
from src.data.drive_bot import DriveBot
import pandas as pd
import matplotlib.pyplot as plt

bot = TelegramBot()
bot.start()
# drive_bot = DriveBot()
# print(drive_bot.get_data())


# from src.visualization.visualize import (
#     barv_aniversariantes_by,
#     hist_aniversariantes_by
# )


# file = pd.read_csv(
#     'data/raw/aniversariantes_anpla.csv',
#     parse_dates=['Data de Nascimento'],
#     dayfirst=True
# )


# meses = {
#     1: 'Janeiro',
#     2: 'Fevereiro',
#     3: 'Março',
#     4: 'Abril',
#     5: 'Maio',
#     6: 'Junho',
#     7: 'Julho',
#     8: 'Agosto',
#     9: 'Setembro',
#     10: 'Outubro',
#     11: 'Novembro',
#     12: 'Dezembro'
# }

# file['Mes'] = file['Data de Nascimento'].dt.month.map(meses)

# ordem_meses = list(meses.values())

# file['Mes'] = pd.Categorical(
#     file['Mes'],
#     categories=ordem_meses,
#     ordered=True
# )


# faixas = [0, 18, 23, 28, 33, 38, 43, 48, 53, 58, 120]

# faixa_etaria = [
#     '0 a 18',
#     '19 a 23',
#     '24 a 28',
#     '29 a 33',
#     '34 a 38',
#     '39 a 43',
#     '44 a 48',
#     '49 a 53',
#     '54 a 58',
#     '59+'
# ]

# file['Faixa'] = pd.cut(
#     file['Idade'],
#     bins=faixas,
#     labels=faixa_etaria,
#     include_lowest=True
# )

# fig = barv_aniversariantes_by(file,'Mes')

# fig = barv_aniversariantes_by(file,'Faixa')

# plt.show()