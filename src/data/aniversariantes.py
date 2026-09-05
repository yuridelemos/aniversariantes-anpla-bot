import pandas as pd


def aniversariantes_do_dia(dataframe):
    """Retorna os registros do dataframe cujo aniversário é hoje."""
    hoje = pd.Timestamp.now()
    filtro = (
        (dataframe['Data de Nascimento'].dt.day == hoje.day) &
        (dataframe['Data de Nascimento'].dt.month == hoje.month)
    )
    return dataframe[filtro]