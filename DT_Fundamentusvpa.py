'''
    Acrescenta LPA e VPA na planilha do Fundamentus
'''
import warnings
warnings.filterwarnings("ignore")
from DT_Fundamentus import dadosFund
import pandas as pd
import requests
header = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}

dfs = dadosFund ()

def LPA_VPA(ticker:str) :
    url=f'https://www.fundamentus.com.br/detalhes.php?papel={ticker}'
    r = requests.get(url, headers=header)
    PA = pd.read_html(r.text, decimal=',', thousands='.',encoding='ISO-8859-1' )[2]
    # print(PA[[4,5]].iloc[1:3])
    return PA[5].iloc[1], PA[5].iloc[2]

lpa = []
vpa=[]
for i,t in enumerate(dfs['Papel']):
    LPA,VPA= LPA_VPA(t)
    lpa.append(LPA)
    vpa.append(VPA)

dfs['LPA'] = lpa
dfs['VPA'] = vpa

dfs.to_csv("data/fundamentuspp.csv" , sep=';' )

## testes ################

url=f'https://www.fundamentus.com.br/detalhes.php?papel=GOAU4'
r = requests.get(url, headers=header)
for i in range(5):
    print (pd.read_html(r.text)[i])