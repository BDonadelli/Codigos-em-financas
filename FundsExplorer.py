from selenium import webdriver
from time import sleep
from datetime import date
today = date.today().strftime('%d/%m/%Y')
import pandas as pd

from selenium.webdriver.common.by import By
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

sleep(2)
dados = []
dadosTabela = driver.find_element(By.XPATH,'//div/table[contains(@class,"default-fiis-table__container__table")]')

#print(dadosTabela.text)  

for linha in dadosTabela.find_elements(By.TAG_NAME,"tr") :
     linhaDados = []
     for coluna in linha.find_elements(By.TAG_NAME,"td"):
          # print(coluna)
          linhaDados.append(coluna.text)
     dados.append(linhaDados)

driver.close()


colunas = ['Fundos','Setor','Preço Atual (R$)','Liquidez Diária (R$)',#
          'P/VP','Último Dividendo','Dividend Yield','DY (3M) Acumulado',#
          'DY (6M) Acumulado','DY (12M) Acumulado','DY (3M) média','DY (6M) média',#
          'DY (12M) média','DY Ano','Variação Preço','Rentab. Período','Rentab. Acumulada',#
          'Patrimônio Líquido','VPA','P/VPA','DY Patrimonial','Variação Patrimonial',#
          'Rentab. Patr. Período','Rentab. Patr. Acumulada','Vacância Física',#
          'Vacância Financeira','Quant. Ativos']		
df = pd.DataFrame(dados,columns=colunas)

# Primeiro download um csv com os dados
# depois atualiza planilha no googlesheets

df.to_csv("/home/yair/FundsExplorer.csv")

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/spreadsheets']
jfile = 'carteira-328314-d38dcc8ee3e4.json'

credentials = ServiceAccountCredentials.from_json_keyfile_name(jfile, scope)
gc = gspread.authorize(credentials)

planilha = gc.open('Dados')
pagina = planilha.worksheet("FE")
pagina.clear()

pagina.update('a1',today)
pagina.update('a2',dados)

