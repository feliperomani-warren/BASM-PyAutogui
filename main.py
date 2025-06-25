'''
Esse código é feito com PyAutogui, uma biblioteca de automação de interface gráfica do usuário (GUI) para Python.
Ele permite que você controle o mouse e o teclado para automatizar tarefas repetitivas. 

Portanto ele automatiza cliques na tela e digitação de texto.

A tarefa deste código, é abrir a Bloomberg, acessar a página BASM da Bloomberg, baixar as planilhas de cada mercado de derivativos e B3 e salvar na pasta Adele.
[DOL, WDO, FRP, FRC, DI1, DAP, IND, WIN, BMF geral, B3]

Depois junta esses dados, faz um tratamento, e salva numa planilha do sheets.

Após salvar os dados na planilha do sheets, ele joga os dados pro Databricks.

Para desenvolver essa automação, eu utilizei a videoaula: https://www.youtube.com/watch?v=h9vEE1KWsI4

Também utilizei a documentação do PyAutogui: https://pyautogui.readthedocs.io/en/latest/quickstart.html

1 - Abre o VNC Viewer e conecta na máquina da Bloomberg Sales
2 - Abre o Bloco de Notas e mostra uma mensagem que que tem uma autoamção funcionando
3 - Abre uma nova guia na Bloomberg e acessa a página BASM
4 - Faz um loop para coleta dados de Market Share de cada mercado de derivativos e B3

Para Ajustar pro João, precisar adaptar de uma maneira que ele colete apenas do dia anterior, e não coletar tudo
'''

import pyautogui as pg
import pandas as pd
import time
from pathlib import Path
from datetime import datetime, timedelta
from functions import gerar_dias_uteis, encontrar_imagem_com_timeout,coletar_dados_bbg2

hoje = datetime.now().strftime('%Y-%m-%d')
dias_uteis = gerar_dias_uteis('FeriadosB3.csv')

resposta = pg.confirm(text="Você deseja iniciar a automação para coletar os dados da Bloomberg?\n\n Ela irá acessar o VNC, e coletar os dados de Market Share no BASM.",
           title="Robô Automação 🤖", buttons=["Iniciar Automação", "Cancelar"])

if resposta == "Cancelar":
    pg.alert(text="Automação Cancelada!", title="Robô Automação 🤖")
    exit()


time.sleep(3)
# Iniciando automação

# 1 - Abre o VNC Viewer e conecta na máquina da Bloomberg Sales
# pg.press('win')
# time.sleep(1)

# pg.typewrite('RealVNC Viewer')
# pg.press('enter')
# time.sleep(3)

# pg.typewrite('BBG Sales')
# pg.press('enter')
# time.sleep(3)

# local_barra = encontrar_imagem_com_timeout('BarraVNC3.png', timeout=30, confianca=0.7, regiao=None, intervalo_tentativas=0.5)
# pg.doubleClick(local_barra)
# time.sleep(1)

# 2 - Abre o Bloco de Notas e mostra uma mensagem que que tem uma autoamção funcionando
# clique_bem_sucedido = False
# for tentativa in range(3):
#     print(f"Tentativa {tentativa + 1} de clicar em 'BarraWindows.png'...")
#     try:
#         local_win = encontrar_imagem_com_timeout('BarraWindows.png', timeout=30, confianca=0.7, regiao=None, intervalo_tentativas=0.5)

#         if local_win: 
#             pg.click(local_win)
#             clique_bem_sucedido = True
#             time.sleep(1)
#             break 
#         else:
#             print("'BarraWindows.png' não encontrado nesta tentativa.")
#             if tentativa < 2: 
#                 time.sleep(0.5)

#     except Exception as e:
#         print(f"Ocorreu um erro ao tentar localizar ou clicar em 'BarraWindows.png': {e}")
#         if tentativa < 2:
#              time.sleep(0.5)

# if not clique_bem_sucedido:
#     pg.alert(text="Não foi possível clicar em 'BarraWindows.png' após 3 tentativas. Verifique se o elemento está visível.", title="Robô Automação 🤖 - Erro")
#     print("Falha ao clicar em 'BarraWindows.png' após 3 tentativas.")
#     exit()


# pg.typewrite('Bloco de Notas')
# pg.press('enter')
# time.sleep(1)
# pg.typewrite("🤖 Automacao Bloomberg, espere um pouco...\nQualquer dúvida chama o @Felipe Romani no Slack")

# 3 - Abre uma nova guia na Bloomberg e acessa a página BASM
try:
    nova_guia = encontrar_imagem_com_timeout('ImagemNovaGuiaBBG.png', timeout=2, confianca=0.9, regiao=None, intervalo_tentativas=0.5)
except:
    nova_guia = encontrar_imagem_com_timeout('ImagemNovaGuiaBBG2.png', timeout=2, confianca=0.9, regiao=None, intervalo_tentativas=0.5)

pg.click(nova_guia)
time.sleep(1)
pg.typewrite('BASM')
pg.press('enter')
time.sleep(1)

# 4 - Faz um loop para coleta dados de Market Share de cada mercado de derivativos e B3
mercados_curvas = {
    'BMF': [
        ' ', # BMF Geral, fica sem curva
        'Curva DAP [34] (My Lists - W)',
        'Curva FRC [35] (My Lists - W)',
        'Curva DDI [36] (My Lists - W)',
        'Curva DOL [37] (My Lists - W)',
        'Curva IND [38] (My Lists - W)',
        'Curva WIN [39] (My Lists - W)',
        'Curva DI1 [40] (My Lists - W)',
        'FRPs [41] (My Lists - W)',
        'Curva WDO [42] (My Lists - W)'
    ],
    'BZ': [' '] # BZ siginfica a B3
}

# dias_uteis = [data for data in dias_uteis if data < datetime(2025, 5, 6)] #Estava filtando as datas pois o pessoal precisava mexer na BBG
pasta_downloads = Path(r'\\adele\USERS\#Crossing\Economia X MesaTitulos\Estrategia\Inteligencia Institucional\BASM - BBG')
for mercado, curvas in mercados_curvas.items():
    for curva in curvas:
        for data in dias_uteis:
            # Verifica se o arquivo já existe
            curva_prefixo = curva.split('[')[0].strip()
            nome_arquivo = f'BASM - {mercado} {curva_prefixo} - {data.strftime("%Y-%m-%d")}.xlsx'
            caminho_completo_do_arquivo = pasta_downloads / nome_arquivo
            if caminho_completo_do_arquivo.is_file():
                print(f"Arquivo já existe, pulando: {nome_arquivo}")
                continue

            print(f"Coletando dados para o mercado: {mercado}, curva: '{curva}', data: {data.strftime('%Y-%m-%d')}")
            coletar_dados_bbg2(mercado, curva, data)