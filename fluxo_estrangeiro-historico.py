
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions, Chrome, Keys

#Chrome
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

opts = webdriver.ChromeOptions()
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

path='//*[@id="download-csv"]'
botao = driver.find_element(By.XPATH,path)
botao.click()


import pandas as pd
import sys,csv
import numpy as np

filename = 'fluxo-historico.csv'
with open(filename, "r") as f:
  reader = csv.reader(f, delimiter=',')
  x=list(reader)

a=[]
ind=[]
for l in range(1,len(x)):
  ind.append(x[l][0])
  i=1
  while i < 11 :      
      a.append(x[l][i].replace('.','')+'.'+x[l][i+1][:-3])
      i=i+2

data = np.array( a,dtype=float )
m=data.reshape( len(x)-1 , 5 )
df = pd.DataFrame(m, index=ind  , columns=x[0][1:])
print(df.tail())

driver.close()

import plotly.graph_objects as go

fig = go.Figure(go.Bar(
            x=df.index[::-1] , 
            y=df.Estrangeiro[::-1] ,
            orientation='v'))

fig.show()