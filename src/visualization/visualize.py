import io
import matplotlib.pyplot as plt
import numpy as np

def barv_aniversariantes_by(dataframe, axisX):
    resultado = dataframe.groupby(axisX, observed=True).size()
    total = resultado.sum()

    fig, ax = plt.subplots()

    barras = ax.bar(resultado.index, resultado.values, zorder=3)

    ax.set_xlabel(axisX)
    ax.set_ylabel('Quantidade de Pessoas')
    ax.set_title(f'Distribuição por {axisX}  (Total: {total})')

    ax.tick_params(axis='x', rotation=45) # Rotacionar um pouco para conseguir ler melhor o texto do eixo X

    max_valor = resultado.values.max()
    passo = 5
    limite = int(np.ceil((max_valor + passo) / passo) * passo)
    ax.set_yticks(np.arange(0, limite, passo))

    # Linhas horizontais de grade, atrás das barras que vão Ajudar a visualizar melhor
    ax.grid(axis='y', linestyle='--', alpha=0.6, zorder=0)

    # Mostrar o valor em cima de cada barra para ajudar a visualizar melhor
    ax.bar_label(barras, padding=3)

    fig.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    plt.close(fig)

    return buf


# def hist_aniversariantes_by(dataframe, axisX):
#     fig, ax = plt.subplots()

#     ax.hist(dataframe[axisX], bins=20)

#     ax.set_xlabel(axisX)
#     ax.set_ylabel('Quantidade de Aniversariantes')
#     ax.set_title(f'Distribuição por {axisX}')

#     fig.tight_layout()
#     fig.savefig(f'hist_aniversariantes_by_{axisX}.png')

#     plt.close(fig)
