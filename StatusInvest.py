rm = 's'#input('remover arquivos (s/n)?')
if rm =='s':
    import os
    import glob
    pattern = r"/home/yair/GHub/Codigos-em-financas/statusinvest-busca-avancada*"

    try:
        for item in glob.iglob(pattern, recursive=True):
            os.remove(item)
    except: print('não há arquivo')


from selenium import webdriver
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions, Chrome, Keys

#Chrome
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

opts = ChromeOptions()
#esta opcao serve para nao fechar o navegador apos a execucao do script
opts.add_experimental_option("detach", True)
opts.add_experimental_option("prefs", {
  "download.default_directory": r"/home/yair/GHub/Codigos-em-financas/data/",
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True
})

servico=Service(ChromeDriverManager().install())
driver=webdriver.Chrome(service=servico, options=opts)

url1='https://statusinvest.com.br/acoes/busca-avancada'
url2='https://statusinvest.com.br/fundos-imobiliarios/busca-avancada'
url3='https://statusinvest.com.br/acoes/eua/busca-avancada'

#############
driver.get(url1)
sleep(4)

path='//div/button[contains(@class,"find")]'
path2='//div/a[contains(@class,"btn-download")]'

driver.find_element(By.XPATH,path).click()
sleep(20)#espera anuncio
# anuncio = 
driver.find_elements(By.CLASS_NAME,'btn-close')[0].click()
sleep(3)
# download
driver.find_element(By.XPATH,path2).click()

sleep(15)
### driver.close()

import pandas as pd


df = pd.read_csv('statusinvest-busca-avancada.csv', 
                 sep=';' , decimal=',' , header = 0, index_col=False ,  thousands='.' , 
                 encoding='latin1')
df = df.fillna('')

print(df.head())


# agora atualiza planilha diretamente no googlesheets
import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = ['https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/spreadsheets']
jfile = 'carteira-328314-d38dcc8ee3e4.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(jfile, scope)
gc = gspread.authorize(credentials)

planilha = gc.open('Dados')
pagina = planilha.worksheet("StatusInvest-Acoes")


pagina.update('b2', [df.columns.values.tolist()] + df.values.tolist())
# # registra data da ultima atualização
from datetime import date
pagina.update('a1',date.today().strftime('%d/%m/%Y'))

##############

driver.get(url2)
sleep(4)

path='//div/button[contains(@class,"find")]'
path2='//div/a[contains(@class,"btn-download")]'

driver.find_element(By.XPATH,path).click()
sleep(5)
# download
driver.find_element(By.XPATH,path2).click()

sleep(15)
driver.close()

df2 = pd.read_csv('statusinvest-busca-avancada (1).csv', 
                 sep=';' , decimal=',' , header = 0, index_col=False ,  thousands='.' , 
                 encoding='latin1')
df2 = df2.fillna('')

print(df2.head())

# agora atualiza planilha diretamente no googlesheets
import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = ['https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/spreadsheets']
jfile = 'carteira-328314-d38dcc8ee3e4.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(jfile, scope)
gc = gspread.authorize(credentials)

planilha = gc.open('Dados')
pagina = planilha.worksheet("StatusInvest-FIIs")


pagina.update('b2', [df2.columns.values.tolist()] + df2.values.tolist())
# # registra data da ultima atualização
from datetime import date
pagina.update('a1',date.today().strftime('%d/%m/%Y'))

