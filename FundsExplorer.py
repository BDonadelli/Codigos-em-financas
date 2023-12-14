import pandas as pd
from selenium import webdriver
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from selenium.webdriver import ChromeOptions, Chrome, Keys
#Chrome
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


opts = ChromeOptions()
##esta opcao serve para nao fechar o navegador apos a execucao do script
opts.add_experimental_option("detach", True)
servico=Service(ChromeDriverManager().install())
driver=webdriver.Chrome(service=servico, options=opts)

driver.get("https://www.fundsexplorer.com.br/ranking")
# driver.maximize_window()
sleep(5)
# Scroll up the window by a specific number of pixels
# For example, scroll up by 200 pixels
scroll_distance = 400
driver.execute_script(f"window.scrollBy(0, {scroll_distance});")
sleep(2)

colunas = ['Fundos','Setor','Preço Atual (R$)','Liquidez Diária (R$)',#
          'P/VP','Último Dividendo','Dividend Yield','DY (3M) Acumulado',#
          'DY (6M) Acumulado','DY (12M) Acumulado','DY (3M) média','DY (6M) média',#
          'DY (12M) média','DY Ano','Variação Preço','Rentab. Período','Rentab. Acumulada',#
          'Patrimônio Líquido','VPA','P/VPA','DY Patrimonial','Variação Patrimonial',#
          'Rentab. Patr. Período','Rentab. Patr. Acumulada','Quant. Ativos' ,'Volatilidade' , #
          'Num. Cotistas' , 'Tax. Gestão' , 'Tax. Performance' , 'Tax. Administração']

driver.find_element(By.XPATH,'//*[@id="colunas-ranking__select-button"]').click()
sleep(5)
driver.find_element(By.XPATH,'/html/body/div[6]/div[1]/div/div[2]/div[2]/ul/li[1]/label/span').click()
sleep(5)

dados = [colunas]
dadosTabela = driver.find_element(By.XPATH,'//div/table[contains(@class,"default-fiis-table__container__table")]')

# print(dadosTabela.text)  

for linha in dadosTabela.find_elements(By.TAG_NAME,"tr") :
     linhaDados = []
     for coluna in linha.find_elements(By.TAG_NAME,"td"):
          # print(coluna)
          linhaDados.append(coluna.text)
     dados.append(linhaDados)

driver.close()

df = pd.DataFrame(dados)#,columns=colunas)

# Primeiro faz download  de um csv com os dados
df.to_csv("/home/yair/GHub/Codigos-em-financas/FundsExplorer.csv")

# agora atualiza planilha diretamente no googlesheets

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/spreadsheets']
jfile = 'destrincha-fatura.json'

credentials = ServiceAccountCredentials.from_json_keyfile_name(jfile, scope)
gc = gspread.authorize(credentials)

planilha = gc.open('Dados')
pagina = planilha.worksheet("teste")

pagina.clear()
pagina.update('a2',dados)
# registra data da ultima atualização
from datetime import date
pagina.update('a1',date.today().strftime('%d/%m/%Y'))
driver.quit()