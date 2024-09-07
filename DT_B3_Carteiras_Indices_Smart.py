'''
    Download de carteiras teóricas  da B3
        - Índice Bovespa Smart Low Volatility B3, é um índice de retorno total.
        indicador de desempenho médio dos ativos de maior negociabilidade, representatividade e que possuem menor volatilidade nos retornos diários.
        metodologia: https://www.b3.com.br/data/files/A5/34/90/0A/E28B09105FE89209AC094EA8/Metodologia_IbovLowVolB3_PT.pdf
        - Índice Bovespa Smart High Beta B3 , é um índice de retorno total.
        indicador de desempenho médio dos ativos de maior negociabilidade, representatividade e que possuem maior sensibilidade às mudanças nos retornos do mercado. Essa relação é medida pelo beta individual de cada ativo
        metodologia: https://www.b3.com.br/pt_br/market-data-e-indices/indices/indices-de-segmentos-e-setoriais/ibov-smart-high-beta-b3-composicao-da-carteira.htm

'''

import pandas as pd
import os
from DT_atualiza_settings import *

url=[
    'https://www.b3.com.br/pt_br/market-data-e-indices/indices/indices-de-segmentos-e-setoriais/ibov-smart-low-vol-b3-composicao-da-carteira.htm',
    'https://www.b3.com.br/pt_br/market-data-e-indices/indices/indices-de-segmentos-e-setoriais/ibov-smart-high-beta-b3-composicao-da-carteira.htm'
]

driver=webdriver.Chrome(options=opts)
for sitio in  url :
    driver.get(sitio)
    if sitio == url[0] :
       driver.find_element(By.ID,'onetrust-accept-btn-handler').click()
       driver.implicitly_wait(3) # seconds
    driver.switch_to.frame("bvmf_iframe")
    driver.find_element(By.CLASS_NAME , 'primary-text').find_element(By.TAG_NAME,"a").click()
    sleep(3)
driver.close()    

'''
    remanejo dos nomes dos arquivos 
'''

for filename in os.listdir(data_path):
    if 'Cart_' in filename:
        os.remove(data_path+filename)


files_dict = {'IBLVDia':'Cart_Ibov_LowVol',
              'IBHBDia':'Cart_Ibov_HighBeta'}

for chave in files_dict.keys(): 
    for filename in os.listdir(data_path):
        if chave in filename:
            os.rename(data_path+filename,data_path+files_dict[chave]+'.csv')

for filename in os.listdir(data_path):
    if "Cart_Ibov" in filename:
        # print(filename)
        df=pd.DataFrame()
        df= pd.read_csv(data_path+filename, encoding='latin-1', index_col=False, sep=';', decimal=',', thousands='.',
                        skiprows=[0],skipfooter=2,engine='python'
                        )
        df= df.sort_values(by='Part. (%)',ascending =False)
        df.to_csv(data_path+filename,index=None)#,sep=';')
        print(df)
