# def concatenar_excels(caminho_pasta, sheet_name=0):
#     import os
#     import pandas as pd
    
#     dfs = []
#     for arquivo in os.listdir(caminho_pasta):
#         if arquivo.endswith('.xlsx') or arquivo.endswith('.xls'):
#             caminho_arquivo = os.path.join(caminho_pasta, arquivo)
#             try:
#                 df = pd.read_excel(caminho_arquivo, sheet_name=sheet_name)
#                 df['arquivo_origem'] = arquivo  # opcional: ajuda a rastrear de qual arquivo veio
#                 dfs.append(df)
#             except Exception as e:
#                 print(f"Erro ao ler {arquivo}: {e}")
    
#     if dfs:
#         df_final = pd.concat(dfs, ignore_index=True)
#         return df_final
#     else:
#         return pd.DataFrame()
    
    
import os
import pandas as pd

dfs = []
for arquivo in os.listdir(r'\\adele\USERS\#Crossing\Economia X MesaTitulos\Estrategia\Inteligencia Institucional\BASM - BBG'):
    if arquivo.endswith('.xlsx') or arquivo.endswith('.xls'):
        caminho_arquivo = os.path.join(r'\\adele\USERS\#Crossing\Economia X MesaTitulos\Estrategia\Inteligencia Institucional\BASM - BBG', arquivo)

        print(f"Lendo arquivo: {arquivo}")
        df = pd.read_excel(caminho_arquivo, sheet_name='Worksheet', header=4)
        df['arquivo_origem'] = arquivo  # opcional: ajuda a rastrear de qual arquivo veio
        print(df["arquivo_origem"].str.split(" - ", expand=True))
        df[["prefixo", "curva", "data"]] = df["arquivo_origem"].str.split(" - ", expand=True)
        df['data'] = df['data'].str.replace('.xlsx', '')
        df = df[df['Broker code'] != 'Totals']
        # df['Broker short name'] = df["Broker name"].str.split(" ", expand=True)[0]
        dfs.append(df)

if dfs:
    df_final = pd.concat(dfs, ignore_index=True)
    print(df_final)
    df_final.to_csv(r'\\adele\USERS\#Crossing\Economia X MesaTitulos\Estrategia\Inteligencia Institucional\BASM - PyAutogui\df_final.csv', index=False)