import pandas as pd
try:
    xls = pd.ExcelFile('Desemprego.xlsx', engine='openpyxl')
    print(xls.sheet_names)
except Exception as e:
    print(f"Erro ao ler o arquivo: {e}")
