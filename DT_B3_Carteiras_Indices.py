'''
    Downloada de carteiras teóricas de vários indicies da B3

Ibov -  85% em ordem decrescente de Índice de Negociabilidade; 
        95% de presença em pregão; 0,1% do volume financeiro no mercado a vista (lote-padrão); e não ser penny stock.
IBrx100 -   os 100 primeiros ativos em ordem decrescente de Índice de Negociabilidade; 
            95% de presença em pregão; e não ser penny stock.
IBrx50 - os 50 primeiros ativos em ordem decrescente de Índice de Negociabilidade; 
         95% de presença em pregão; e não ser penny stock.
IBrA -  99% em ordem decrescente de Índice de Negociabilidade; 95% de presença em pregão; e não ser penny stock.            
B3 BR+ - ações, units e BDRs de empresas brasileiras listadas na B3 No que tange os BDRs, é necessário que a listagem primária do ativo lastro seja feita nas bolsas de valores dos Estados Unidos (EUA).
'''

import pandas as pd
import os
from DT_atualiza_settings import *

url=[
    'https://www.b3.com.br/pt_br/market-data-e-indices/indices/indices-amplos/indice-brasil-amplo-ibra-composicao-da-carteira.htm',
    'https://www.b3.com.br/pt_br/market-data-e-indices/indices/indices-amplos/indice-brasil-100-ibrx-100-composicao-da-carteira.htm',   #IBR100
    'https://www.b3.com.br/pt_br/market-data-e-indices/indices/indices-amplos/indice-brasil-50-ibrx-50-composicao-da-carteira.htm',     #IBR50
    'https://www.b3.com.br/pt_br/market-data-e-indices/indices/indices-amplos/indice-ibovespa-ibovespa-composicao-da-carteira.htm',     #IBOV
    'https://www.b3.com.br/pt_br/market-data-e-indices/indices/indices-de-segmentos-e-setoriais/indice-dividendos-idiv-composicao-da-carteira.htm', #IDIV
    'https://www.b3.com.br/pt_br/market-data-e-indices/indices/indices-de-segmentos-e-setoriais/indice-small-cap-smll-composicao-da-carteira.htm',
    'https://www.b3.com.br/pt_br/market-data-e-indices/indices/indices-de-segmentos-e-setoriais/indice-fundos-de-investimentos-imobiliarios-ifix-composicao-da-carteira.htm',
    'https://www.b3.com.br/pt_br/market-data-e-indices/indices/indices-amplos/indice-bovespa-b3-br-ibovespa-b3-br-composicao-carteira.htm'
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
    remanejo dos nomes dos arquivos -------------------------------------------
'''

for filename in os.listdir(data_path):
    if 'Cart_' in filename and 'Smart' not in filename:
        os.remove(data_path+filename)

files_dict = {'IBOVDia':'Cart_Ibov',
            'IBRADia':'Cart_IBrA',
            'SMLLDia':'Cart_Small',
            'IBXXDia':'Cart_IBr100',
            'IBXLDia':'Cart_IBr50',
            'IDIVDia':'Cart_Idiv',
            'IFIXDia':'Cart_Ifix',
            'IBBRDia' : 'Cart_IBBR'}

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
