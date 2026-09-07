import pandas as pd
import numpy as np

def transform_dataframe(dataframe):
    # Convert the 'Data de Nascimento' column to datetime format
    dataframe['Data de Nascimento'] = pd.to_datetime(dataframe['Data de Nascimento'], format='%d/%m/%Y')

    # Calculate the age of each person based on their date of birth
    today = pd.Timestamp.now()
    dataframe['Idade'] = (today - dataframe['Data de Nascimento']).dt.days // 365

    meses = {
        1: 'Janeiro',
        2: 'Fevereiro',
        3: 'Março',
        4: 'Abril',
        5: 'Maio',
        6: 'Junho',
        7: 'Julho',
        8: 'Agosto',
        9: 'Setembro',
        10: 'Outubro',
        11: 'Novembro',
        12: 'Dezembro'
    }

    dataframe['Mes'] = (
        dataframe['Data de Nascimento']
        .dt.month
        .map(meses)
    )

    ordem_meses = list(meses.values())

    dataframe['Mes'] = pd.Categorical(
        dataframe['Mes'],
        categories=ordem_meses,
        ordered=True
    )
    
    # Define age ranges and corresponding labels
    bins = [0, 18, 30, 40, 50, 60, np.inf]
    labels = ['0-17', '18-29', '30-39', '40-49', '50-59', '60+']

    # Create a new column for age ranges
    dataframe['Faixa Etária'] = pd.cut(dataframe['Idade'], bins=bins, labels=labels, right=False)

    return dataframe