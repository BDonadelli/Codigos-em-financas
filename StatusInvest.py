
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
  "download.default_directory": r"/home/yair/GHub",
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True
})

servico=Service(ChromeDriverManager().install())
driver=webdriver.Chrome(service=servico, options=opts)

url1='https://statusinvest.com.br/acoes/busca-avancada'
url2='https://statusinvest.com.br/fundos-imobiliarios/busca-avancada'
url3='https://statusinvest.com.br/acoes/eua/busca-avancada'

driver.get(url1)

sleep(4)

path='//div/button[contains(@class,"find")]'
path2='//div/a[contains(@class,"btn-download")]'

botao = driver.find_element(By.XPATH,path)
botao.click()
sleep(20)

anuncio = driver.find_elements(By.CLASS_NAME,'btn-close')[0]
#print(anuncio)
anuncio.click()
sleep(3)

download = driver.find_element(By.XPATH,path2)
download.click()

# driver.close()
# driver=webdriver.Chrome(service=servico, options=opts)

driver.get(url2)

sleep(4)

path='//div/button[contains(@class,"find")]'
path2='//div/a[contains(@class,"btn-download")]'

botao = driver.find_element(By.XPATH,path)
botao.click()
sleep(5)

# anuncio = driver.find_elements(By.CLASS_NAME,'btn-close')[0]
# # #print(anuncio)
# anuncio.click()
# sleep(3)

download = driver.find_element(By.XPATH,path2)
download.click()

# driver.close()
# driver=webdriver.Chrome(service=servico, options=opts)

driver.get(url3)

sleep(4)

path='//div/button[contains(@class,"find")]'
path2='//div/a[contains(@class,"btn-download")]'

botao = driver.find_element(By.XPATH,path)
botao.click()
sleep(5)

# anuncio = driver.find_elements(By.CLASS_NAME,'btn-close')[0]
# # #print(anuncio)
# anuncio.click()
# sleep(3)

download = driver.find_element(By.XPATH,path2)
download.click()

# rm = input('remover arquivos (s/n)?')
# if rm =='s':
#     import os
#     try:
#         os.remove('/home/yair/Dropbox/Desktop/statusinvest-busca-avancada.csv')
#     except: print('não há arquivo')
#     try:
#         os.remove('/home/yair/Dropbox/Desktop/statusinvest-busca-avancada (1).csv')
#     except: print('não há arquivo')

#     try:
#         os.remove('/home/yair/Dropbox/Desktop/statusinvest-busca-avancada (2).csv')
#     except: print('não há arquivo')

print('ok')
driver.close()