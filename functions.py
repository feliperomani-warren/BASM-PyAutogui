def encontrar_imagem_com_timeout(imagem_path, timeout=30, confianca=0.7, regiao=None, intervalo_tentativas=0.5):
    import pyautogui as pg
    import time
    """
    Tenta encontrar uma imagem na tela repetidamente até um timeout.

    Args:
        imagem_path (str): Caminho para o arquivo de imagem.
        timeout (int): Tempo máximo em segundos para tentar encontrar a imagem.
        confianca (float): Nível de confiança para a correspondência da imagem.
        regiao (tuple, optional): Tupla (left, top, width, height) para limitar a área de busca.
        intervalo_tentativas (float): Tempo em segundos entre as tentativas.

    Returns:
        tuple: As coordenadas (left, top, width, height) e o centro da imagem se encontrada,
               ou None se não encontrada dentro do timeout.
    """
    print(f"Procurando por '{imagem_path}' por até {timeout} segundos...")
    tempo_inicial = time.time()
    while (time.time() - tempo_inicial) < timeout:
        try:
            posicao_centro = pg.locateCenterOnScreen(imagem_path, confidence=confianca, region=regiao) # Tenta localizar no centro para clicar diretamente
            if posicao_centro:
                print(f"Imagem '{imagem_path}' encontrada em: {posicao_centro}")
                return posicao_centro
            else:
                pass
        except pg.ImageNotFoundException:
            pass
        except Exception as e:
            print(f"Erro inesperado ao procurar '{imagem_path}': {e}") # Captura outros erros inesperados durante a tentativa
            pass
        time.sleep(intervalo_tentativas) # Espera antes da próxima tentativa

    print(f"Timeout: Imagem '{imagem_path}' não encontrada após {timeout} segundos.")
    return None

##########################################################################################################################
def gerar_dias_uteis(feriados_path):
    from datetime import datetime, timedelta
    import pandas as pd
    
    ontem = datetime.today() - timedelta(days=1) 
    um_ano_atras = ontem - timedelta(days=365)

    feriados_df = pd.read_csv(feriados_path)
    feriados_df['data'] = pd.to_datetime(feriados_df['data'])
    feriados = set(feriados_df['data'].dt.date)

    dias_uteis = []
    data_atual = um_ano_atras
    while data_atual <= ontem:
        if data_atual.weekday() < 5 and data_atual.date() not in feriados:
            dias_uteis.append(data_atual)
        data_atual += timedelta(days=1)

    return dias_uteis[::-1]

##########################################################################################################################


def coletar_dados_bbg2(mercado, curva, data):
    import time
    import pyautogui as pg
    from functions import encontrar_imagem_com_timeout
    """
    Função para coletar dados do BASM da Bloomberg para um mercado específico e .
    """
    # 2 - Acessar a página BASM da Bloomberg
    try:
        filtro_exchange_basm = encontrar_imagem_com_timeout('FiltroExchangeBASM.png', timeout=30, confianca=0.75, regiao=None, intervalo_tentativas=0.5)
    except:
        filtro_exchange_basm = encontrar_imagem_com_timeout('FiltroExchangeBASM2.png', timeout=30, confianca=0.75, regiao=None, intervalo_tentativas=0.5)
        
    pg.doubleClick(filtro_exchange_basm)
    time.sleep(1)
    pg.typewrite(mercado)                                                                
    pg.press('tab')
    pg.typewrite('Date')
    pg.press('tab')
    pg.typewrite(data.strftime('%m%d%y'))
    pg.press('tab')
    pg.press('tab') #Vai para a caixa de List Filter
    pg.typewrite(curva)
    time.sleep(1)
    pg.press('enter')
    
    time.sleep(1)
    botao_export = encontrar_imagem_com_timeout('Export.png', timeout=30, confianca=0.75, regiao=None, intervalo_tentativas=0.5)
    pg.click(botao_export)#Clicando no botao Export

    time.sleep(2)
    botao_current_view = encontrar_imagem_com_timeout('BotaoCurrentView.png', timeout=30, confianca=0.75, regiao=None, intervalo_tentativas=0.5)
    pg.click(botao_current_view)
    
    
    time.sleep(6) #Espera o excel abrir

    excel =encontrar_imagem_com_timeout('CliqueExcel.png', timeout=30, confianca=0.75, regiao=None, intervalo_tentativas=0.5)
    pg.doubleClick(excel)
    time.sleep(1)
    pg.hotkey('fn','f12') # Abre a janela de salvar como no Excel
    time.sleep(1.5)

    exp = encontrar_imagem_com_timeout('BarraPesquisaExploradorDeArquivo.png', timeout=30, confianca=0.75, regiao=None, intervalo_tentativas=0.5)
    pg.doubleClick(exp)
    time.sleep(1)
    pg.hotkey('ctrl','a')
    pg.typewrite('Z:\Inteligencia Institucional\BASM - BBG')
    pg.press('enter') # Vai para a pasta de downloads
    pg.press('tab') # Vai para a caixa de nome do arquivo
    pg.press('tab')
    pg.press('tab')
    pg.press('tab')
    pg.press('tab')
    pg.press('tab')
    time.sleep(1)
    pg.typewrite(f'BASM - {mercado} {curva.split('[')[0].strip()} - {data.strftime("%Y-%m-%d")}') # Digita o nome do arquivo
    pg.press('enter') #Salva o arquivo

    pg.hotkey('alt','f4') # fecha o excel

    time.sleep(1)
    
##############################################################################################################################################
# Adicione esta função ao seu arquivo functions.py

def encontrar_ponto_de_retomada(pasta_path, mercados_curvas):
    """
    Verifica a pasta de downloads para encontrar o último arquivo salvo e
    determina de onde a automação deve continuar.

    Args:
        pasta_path (str): Caminho para a pasta onde os arquivos são salvos.
        mercados_curvas (dict): Dicionário com a estrutura de mercados e curvas.

    Returns:
        tuple: (mercado, curva, data) do último arquivo salvo, ou (None, None, None) se a pasta está vazia.
    """
    import os
    from datetime import datetime

    try:
        # Lista apenas os arquivos .xlsx para evitar outros tipos de arquivos
        arquivos = [f for f in os.listdir(pasta_path) if f.startswith('BASM -') and f.endswith('.xlsx')]
        if not arquivos:
            print("Nenhum arquivo de progresso encontrado. Iniciando do zero.")
            return None, None, None

        # Encontra o arquivo mais recente com base na data de modificação
        caminho_completo_arquivos = [os.path.join(pasta_path, f) for f in arquivos]
        ultimo_arquivo_path = max(caminho_completo_arquivos, key=os.path.getmtime)
        ultimo_arquivo_nome = os.path.basename(ultimo_arquivo_path)
        
        print(f"Último arquivo encontrado: {ultimo_arquivo_nome}")

        # --- Extrai a data do nome do arquivo ---
        try:
            # Pega a parte da data no final do nome do arquivo '... - AAAA-MM-DD.xlsx'
            data_str = ultimo_arquivo_nome.split(' - ')[-1].replace('.xlsx', '')
            ultima_data = datetime.strptime(data_str, '%Y-%m-%d')
        except (ValueError, IndexError):
            print(f"Aviso: Não foi possível extrair a data do arquivo '{ultimo_arquivo_nome}'. Iniciando do zero.")
            return None, None, None

        # --- Encontra o mercado e a curva correspondentes ---
        for mercado, curvas in mercados_curvas.items():
            for curva in curvas:
                # Recria a parte do nome do arquivo como a função de coleta faz
                curva_prefixo = curva.split('[')[0].strip()
                # O strip() no final remove o espaço extra para 'BMF Geral' e 'B3'
                nome_base_esperado = f"BASM - {mercado} {curva_prefixo}".strip()
                
                if nome_base_esperado in ultimo_arquivo_nome:
                    print(f"Retomada identificada: Mercado='{mercado}', Curva='{curva}', Data='{ultima_data.strftime('%Y-%m-%d')}'")
                    return mercado, curva, ultima_data

        print("Aviso: Arquivo mais recente não corresponde a nenhuma configuração. Iniciando do zero.")
        return None, None, None

    except FileNotFoundError:
        print(f"A pasta '{pasta_path}' não foi encontrada. Verifique o caminho. Iniciando do zero.")
        return None, None, None
    except Exception as e:
        print(f"Ocorreu um erro ao verificar o ponto de retomada: {e}. Iniciando do zero.")
        return None, None, None