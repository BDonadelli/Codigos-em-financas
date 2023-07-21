
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions, Chrome, Keys
#Chrome
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

opts = ChromeOptions()
#esta opcao serve para nao fechar o navegador apos a execucao do script
opts.add_experimental_option("detach", True)
opts.add_experimental_option("prefs", {
  "download.default_directory": r"/home/yair/GHub/Codigos-em-financas/",
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True
})

servico=Service(ChromeDriverManager().install())
driver=webdriver.Chrome(service=servico, options=opts)

from time import sleep

url='https://www.dadosdemercado.com.br/bolsa/investidores-estrangeiros'
driver.get(url)
sleep(2)

# path='//*[@id="download-csv"]'
# botao = driver.find_element(By.XPATH,path)
# botao.click()

print('ok')
driver.close()