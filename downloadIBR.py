
from selenium import webdriver
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions

#Chrome
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

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

url='https://www.b3.com.br/pt_br/market-data-e-indices/indices/indices-amplos/indice-brasil-100-ibrx-100-composicao-da-carteira.htm'

driver.get(url)

sleep(2)
driver.find_element(By.ID,'onetrust-accept-btn-handler').click()

driver.implicitly_wait(3) # seconds

driver.switch_to.frame("bvmf_iframe")

driver.find_element(By.XPATH,'//*[@id="divContainerIframeB3"]/div/div[1]/form/div[2]/div/div[2]/div/div/div[1]/div[2]/p/a').click()
