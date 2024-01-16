
import pandas as pd
from time import sleep
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = "vscode"
from datetime import datetime, date

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
servico=Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=servico) #driver da sua versão

data_di = date.today().strftime('%d/%m/%Y') 

url = f'''https://www2.bmf.com.br/pages/portal/bmfbovespa/boletim1/SistemaPregao1.asp?
pagetype=pop&caminho=Resumo%20Estat%EDstico%20-%20Sistema%20Preg%E3o&Data={data_di}
&Mercadoria=DI1'''

driver.get(url)

path_tabela = '/html/body/div/div[2]/form[1]/table[3]/tbody/tr[3]/td[3]/table'
elemento = driver.find_element(By.XPATH, path_tabela)
html_tabela = elemento.get_attribute('outerHTML')
tabela = pd.read_html(html_tabela)[0]
print(tabela)

sleep(5)

path_indice = '/html/body/div/div[2]/form[1]/table[3]/tbody/tr[3]/td[1]/table'        
elemento_indice = driver.find_element(By.XPATH, path_indice)
html_indice = elemento_indice.get_attribute('outerHTML')
indice = pd.read_html(html_indice)[0]
print(indice)

driver.quit()


legenda = pd.Series(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                        index = ['F', 'G', 'H', 'J', 'K', 'M', 'N', 'Q', 'U', 'V', 'X', 'Z'])

tabela.columns = tabela.loc[0]
tabela = tabela['ÚLT. PREÇO']
tabela = tabela.drop(0, axis = 0)

indice.columns = indice.loc[0]
indice = indice.drop(0, axis = 0)
tabela.index = indice['VENCTO']

tabela = tabela.astype(int)
tabela = tabela[tabela != 0]
tabela = tabela/1000

lista_datas = []

for indice in tabela.index:
        letra = indice[0]
        ano = indice[1:3]
        mes = legenda[letra]
        data = f"{mes}-{ano}"
        data = datetime.strptime(data, "%b-%y")
        lista_datas.append(data)
     
tabela.index = lista_datas  

tabela = tabela/100

print(tabela)

fig= go.Figure()

fig.add_trace(go.Scatter(x=tabela.index, y=tabela.values, name=f"Curva de Juros",
                        line=dict(color='royalblue', width=2), mode='lines+markers'))

fig.update_layout(yaxis=dict(tickformat=".1%", tickfont=dict(color="black")),
                            xaxis=dict(tickfont=dict(color="black")))

fig.show()
