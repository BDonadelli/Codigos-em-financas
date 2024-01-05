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
###########################################################################
# endereço da planilha 
url2='https://statusinvest.com.br/fundos-imobiliarios/busca-avancada'
# caminho html para o botão "buscar"
path='//div/button[contains(@class,"find")]'
# caminho html para o botão "download"
path2='//div/a[contains(@class,"btn-download")]'

## ações
# abre navegador
driver.get(url2)
# espera carregar a pagina
sleep(3)
# clica em buscar
driver.find_element(By.XPATH,path).click()
sleep(3)
## espera um anuncio,
#sleep(16) 
## fecha o anuncio clicando no "x"
#driver.find_elements(By.CLASS_NAME,'btn-close')[0].click()
## clica download
driver.find_element(By.XPATH,path2).click()
# espera o download
sleep(15)
# fecha o navegador
driver.quit()
