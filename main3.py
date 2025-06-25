# '''
# Esse código é feito com PyAutogui, uma biblioteca de automação de interface gráfica do usuário (GUI) para Python.
# Ele permite que você controle o mouse e o teclado para automatizar tarefas repetitivas. 

# Portanto ele automatiza cliques na tela e digitação de texto.

# A tarefa deste código, é abrir a Bloomberg, acessar a página BASM da Bloomberg, baixar as planilhas de cada mercado de derivativos e B3 e salvar na pasta Adele.
# [DOL, WDO, FRP, FRC, DI1, DAP, IND, WIN, BMF geral, B3]

# Depois junta esses dados, faz um tratamento, e salva numa planilha do sheets.

# Após salvar os dados na planilha do sheets, ele joga os dados pro Databricks.

# Para desenvolver essa automação, eu utilizei a videoaula: https://www.youtube.com/watch?v=h9vEE1KWsI4

# Também utilizei a documentação do PyAutogui: https://pyautogui.readthedocs.io/en/latest/quickstart.html

# 1 - Abre o VNC Viewer e conecta na máquina da Bloomberg Sales
# 2 - Abre o Bloco de Notas e mostra uma mensagem que que tem uma autoamção funcionando
# 3 - Abre uma nova guia na Bloomberg e acessa a página BASM
# 4 - Faz um loop para coleta dados de Market Share de cada mercado de derivativos e B3

# Para Ajustar pro João, precisar adaptar de uma maneira que ele colete apenas do dia anterior, e não coletar tudo
# '''

# import pyautogui as pg
# import pandas as pd
# import time
# from datetime import datetime, timedelta
# # Importe a nova função aqui
# from functions import gerar_dias_uteis, encontrar_imagem_com_timeout, coletar_dados_bbg2, encontrar_ponto_de_retomada

# hoje = datetime.now().strftime('%Y-%m-%d')
# dias_uteis = gerar_dias_uteis('FeriadosB3.csv')

# resposta = pg.confirm(text="Você deseja iniciar a automação para coletar os dados da Bloomberg?\n\n Ela irá acessar o VNC, e coletar os dados de Market Share no BASM.",
#            title="Robô Automação 🤖", buttons=["Iniciar Automação", "Cancelar"])

# if resposta == "Cancelar":
#     pg.alert(text="Automação Cancelada!", title="Robô Automação 🤖")
#     exit()

# mercados_curvas = {
#     'BMF': [
#         ' ', # BMF Geral, fica sem curva
#         'Curva DAP [34] (My Lists - W)',
#         'Curva FRC [35] (My Lists - W)',
#         'Curva DDI [36] (My Lists - W)',
#         'Curva DOL [37] (My Lists - W)',
#         'Curva IND [38] (My Lists - W)',
#         'Curva WIN [39] (My Lists - W)',
#         'Curva DI1 [40] (My Lists - W)',
#         'FRPs [41] (My Lists - W)',
#         'Curva WDO [42] (My Lists - W)'
#     ],
#     'BZ': [' '] # BZ siginfica a B3
# }

# # --- LÓGICA DE RETOMADA ---
# # Defina o caminho para a pasta de downloads.
# # ATENÇÃO: Use r'...' (raw string) ou '\\' para evitar problemas com barras invertidas no caminho.
# pasta_downloads = r'Z:\Inteligencia Institucional\BASM - BBG' 

# # Encontra o último ponto de progresso
# mercado_retomada, curva_retomada, data_retomada = encontrar_ponto_de_retomada(pasta_downloads, mercados_curvas)

# # Se não houver ponto de retomada, começará do início. Caso contrário, precisa encontrar onde parar.
# iniciar_coleta = (mercado_retomada is None)

# time.sleep(3)
# # As seções comentadas de VNC e Bloco de Notas permanecem iguais
# # ...

# # 3 - Abre uma nova guia na Bloomberg e acessa a página BASM
# try:
#     nova_guia = encontrar_imagem_com_timeout('ImagemNovaGuiaBBG.png', timeout=2, confianca=0.9, regiao=None, intervalo_tentativas=0.5)
# except:
#     nova_guia = encontrar_imagem_com_timeout('ImagemNovaGuiaBBG2.png', timeout=2, confianca=0.9, regiao=None, intervalo_tentativas=0.5)

# pg.click(nova_guia)
# time.sleep(1)
# pg.typewrite('BASM')
# pg.press('enter')
# time.sleep(1)


# # Loop principal com a lógica de retomada
# for mercado, curvas in mercados_curvas.items():
#     for curva in curvas:
#         for data in dias_uteis:
#             # Verifica se já pode começar a coletar
#             if not iniciar_coleta:
#                 # Se a combinação atual for a mesma que a última salva,
#                 # marca que a PRÓXIMA iteração deve ser coletada e pula a atual.
#                 if mercado == mercado_retomada and curva == curva_retomada and data == data_retomada:
#                     iniciar_coleta = True
#                     print("\n--- Ponto de retomada encontrado. Continuando a coleta a partir do próximo item. ---\n")
#                     continue # Pula para o próximo item do loop (a próxima data/curva/mercado)
#                 else:
#                     # Se ainda não chegou no ponto de retomada, simplesmente continue procurando
#                     continue

#             # Se 'iniciar_coleta' for True, o código a partir daqui será executado.
#             print(f"Coletando dados para o mercado: {mercado}, curva: {curva}, data: {data.strftime('%Y-%m-%d')}")
#             coletar_dados_bbg2(mercado, curva, data)

# pg.alert("Automação finalizada!", "Robô Automação 🤖")