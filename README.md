Link documentação: https://www.canva.com/design/DAGm5ISg8SA/wtd-QYAmYPumaWtQso5tJw/edit?utm_content=DAGm5ISg8SA&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton

Esse projeto inicial é uma "Pipeline" que acessa o Terminal da Bloomberg pelo VNCViewer e baixa diversos arquivos de market share e salva na pasta local '\\adele\USERS\#Crossing\Economia X MesaTitulos\Estrategia\Inteligencia Institucional\BASM - BBG', depois faz um tratamento que agrega todos estes dados, e salva no df_final.csv, que depois é disponibilizado no analysts.felipe_romani.basm_mkt_share_corretoras

Os arquivos mais importantes do projeto são:
main.py (Que funciona com a blommberg pelo VNC VIEWER coletando os dados)
main2.py (que faz o trabalho de agregar todos os arquivos baixados pelo main.py)
