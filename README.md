### 5. Automação BASM Bloomberg

Explicação:

https://www.canva.com/design/DAGm5ISg8SA/wtd-QYAmYPumaWtQso5tJw/edit

- **Objetivo do Projeto:** Automatizar a coleta de dados da plataforma Bloomberg e salvá-los na pasta do servidor adele `\\adele\USERS\#Crossing\Economia X MesaTitulos\Estrategia\Inteligencia Institucional\BASM - BBG`
- O projeto está localizado na pasta do servidor adele `\\adele\USERS\#Crossing\Economia X MesaTitulos\Estrategia\Inteligencia Institucional\BASM - PyAutogui` . O projeto também está disponível no repositório https://github.com/feliperomani-warren/BASM-PyAutogui
- **Tecnologia/Abordagem Atual:** Utiliza automação de busca de imagens e cliques na interface e atalhos do teclado mexendo pelo RealVNC Viewer para interagir com o Terminal Bloomberg.
- **Status:** Pronto. O Joao Varalta pode rodar a automação todos os dias para fazer a coleta de dados. O projeto possivelmente irá evoluir para emails diários
- Os dados serão disponibilizados em uma das tabelas no schema do Databricks e salvando na `analysts.felipe_romani.BASM_mkt_share_corretoras`
- Estes dados substituirão a planilha [`mkt_share_corretoras_anual[NOVA]`](https://docs.google.com/spreadsheets/d/1hQOvSRaY6vOXgBrcb6m7-nKBLfARqsyBP8HAJN96G4Q/edit?usp=drive_open&ouid=102637556264282041211) e da tabela `analysts.felipe_romani.mkt_share_corretoras`
- Ainda é preciso rodar a automação para coletar dados desde o último ano na Bloomberg. Após rodar o código, que é demorado. Haverá diversos excels com dados de operação de cada concorrente a cada dia em cada mercado (Muitos dados). é preciso rodar o `main2.py` Que percorre essa pasta com diversos excel, e unifica em apenas 1 grande df, que será enviado para o databricks `analysts.felipe_romani.BASM_mkt_share_corretoras`
- 
Os arquivos mais importantes do projeto são:
main.py (Que funciona com a blommberg pelo VNC VIEWER coletando os dados)
main2.py (que faz o trabalho de agregar todos os arquivos baixados pelo main.py)
