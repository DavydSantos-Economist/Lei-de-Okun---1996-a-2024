# Este é um script Python puro. Por favor, copie e cole os blocos de código
# em células separadas em um NOVO notebook Jupyter.

# ==============================================================================
# Bloco de Código para a CÉLULA 1
# ==============================================================================
# Objetivo: Instalar dependências e importar todas as bibliotecas necessárias.

# !pip install pandas openpyxl statsmodels matplotlib

import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.tsa.filters import hpfilter
import matplotlib.pyplot as plt

print("Célula 1 executada: Bibliotecas importadas.")


# ==============================================================================
# Bloco de Código para a CÉLULA 2
# ==============================================================================
# Objetivo: Carregar, limpar e unificar os dados de Desemprego e PIB.

# Caminhos para os arquivos de dados
pib_sazonal_path = '6613 - pib 1996 a 2025 com ajuste sazonal.xlsx'
pib_sem_ajuste_path = '6612 - PIB 1996 a 2025 sem ajuste sazonal.xlsx'
desemprego_path = 'Desemprego.xlsx'

try:
    # --- 1. Carregamento e Unificação dos Dados de Desemprego ---
    print("--- Processando dados de desemprego ---")

    # NOTA: Assumindo que as planilhas estão nomeadas 'Sheet1', 'Sheet2', 'Sheet3' em ordem cronológica.
    sheet_names = ['Sheet1', 'Sheet2', 'Sheet3']
    
    try:
        # skiprows=1 assume que a primeira linha de cada planilha é um cabeçalho que pode ser ignorado
        df_pme_antiga = pd.read_excel(desemprego_path, sheet_name=sheet_names[0], engine='openpyxl', skiprows=1)
        df_pme_nova = pd.read_excel(desemprego_path, sheet_name=sheet_names[1], engine='openpyxl', skiprows=1)
        df_pnadc = pd.read_excel(desemprego_path, sheet_name=sheet_names[2], engine='openpyxl', skiprows=1)
    except ValueError as e:
        print(f"ERRO: Uma das planilhas {sheet_names} não foi encontrada. Verifique os nomes no arquivo Excel.")
        raise e

    for df in [df_pme_antiga, df_pme_nova, df_pnadc]:
        df.rename(columns={df.columns[0]: 'Data', df.columns[1]: 'Taxa'}, inplace=True)

    df_pme_antiga['metodologia'] = 'PME_Antiga'
    df_pme_nova['metodologia'] = 'PME_Nova'
    df_pnadc['metodologia'] = 'PNADc'

    df_pme_antiga['Data'] = pd.to_datetime(df_pme_antiga['Data'])
    df_pme_nova['Data'] = pd.to_datetime(df_pme_nova['Data'])
    df_pnadc['Data'] = pd.to_datetime(df_pnadc['Data'])

    df_pme_antiga = df_pme_antiga[df_pme_antiga['Data'].dt.year >= 1994]

    df_desemprego_raw = pd.concat([df_pme_antiga, df_pme_nova, df_pnadc], ignore_index=True)
    df_desemprego_final = df_desemprego_raw.sort_values('Data').drop_duplicates(subset=['Data'], keep='last')

    df_desemprego_final.set_index('Data', inplace=True)
    df_desemprego_final.sort_index(inplace=True)
    df_desemprego_final = df_desemprego_final.loc['1994':'2024']
    
    print("Dados de desemprego unificados com sucesso.")
    print("\n--- Início da série de Desemprego (PME Antiga) ---")
    print(df_desemprego_final.head(3))
    print("\n--- Fim da série de Desemprego (PNADc) ---")
    print(df_desemprego_final.tail(3))
    print("\n--- Contagem de observações por metodologia ---")
    print(df_desemprego_final['metodologia'].value_counts())

    # --- 2. Carregamento dos Dados do PIB ---
    print("\n--- Processando dados do PIB ---")
    # skiprows=1 assume que a primeira linha de cada sheet é um cabeçalho que pode ser ignorado
    df_pib_sazonal = pd.read_excel(pib_sazonal_path, engine='openpyxl', skiprows=1)
    df_pib_sem_ajuste = pd.read_excel(pib_sem_ajuste_path, engine='openpyxl', skiprows=1)
    print("Dados do PIB carregados com sucesso.")
    print("\n--- Amostra do PIB com ajuste sazonal ---")
    print(df_pib_sazonal.head(3))

except FileNotFoundError as e:
    print(f"ERRO: Arquivo não encontrado. Verifique o caminho: {e}")
except Exception as e:
    print(f"Ocorreu um erro inesperado durante o processamento: {e}")

print("\nCélula 2 executada.")
