from selenium import webdriver
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions, Chrome, Keys

#Chrome
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

#opts = ChromeOptions()
#esta opcao serve para nao fechar o navegador apos a execucao do script
#options.add_experimental_option("detach", True)


options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_experimental_option("prefs", {
  "download.default_directory": r"/home/yair/",
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True
})

servico=Service(ChromeDriverManager().install())
driver=webdriver.Chrome(service=servico, options=options)


url=[
    'https://www.b3.com.br/pt_br/market-data-e-indices/indices/indices-amplos/indice-brasil-100-ibrx-100-composicao-da-carteira.htm', #IBR100
    'https://www.b3.com.br/pt_br/market-data-e-indices/indices/indices-amplos/indice-brasil-50-ibrx-50-composicao-da-carteira.htm',#IBR50
    'https://www.b3.com.br/pt_br/market-data-e-indices/indices/indices-amplos/indice-ibovespa-ibovespa-composicao-da-carteira.htm', #IBOV
    'https://www.b3.com.br/pt_br/market-data-e-indices/indices/indices-de-segmentos-e-setoriais/indice-dividendos-idiv-composicao-da-carteira.htm' #IDIV
    ]

for sitio in  url :
    driver.get(sitio)
    sleep(2)
    if sitio == url[0] :
        driver.find_element(By.ID,'onetrust-accept-btn-handler').click()
        driver.implicitly_wait(3) # seconds
    driver.switch_to.frame("bvmf_iframe")
    driver.find_element(By.CLASS_NAME , 'primary-text').find_element(By.TAG_NAME,"a").click()
    sleep(3)

driver.close()    




##XPATH,'//*[@id="divContainerIframeB3"]/div/div[1]/form/div[2]/div/div[2]/div/div/div[1]/div[2]/p/a').click()

#url='https://www.b3.com.br/pt_br/market-data-e-indices/indices/indices-amplos/indice-ibovespa-ibovespa-composicao-da-carteira.htm'
#sleep(2)
#driver.get(url)
#sleep(2)
## driver.find_element(By.ID,'onetrust-accept-btn-handler').click()
## driver.implicitly_wait(3) # seconds
#driver.switch_to.frame("bvmf_iframe")
#driver.find_element(By.XPATH,'//*[@id="divContainerIframeB3"]/div/div[1]/form/div[2]/div/div[2]/div/div/div[1]/div[2]/p/a').click()
