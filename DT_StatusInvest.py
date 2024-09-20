'''
    Esse código baixa planilha de dados fundamentalistas do site Status Invest
            https://statusinvest.com.br/
    e grava em um planilha (privada) do google docs
'''

import warnings
warnings.filterwarnings("ignore")

from  DT_atualiza_settings import *

opcoes_busca = {'Acoes': 'acoes' , 'Fii':'fundos-imobiliarios' , 'Stocks':'acoes/eua'}


def SI(mercado = 'Acoes' , driver=driver) :

    print(f" ====== SI {mercado} ===== ")

    onde = opcoes_busca[mercado]
    url = f'https://statusinvest.com.br/{onde}/busca-avancada'

    driver.get(url)
    
    path='//div/button[contains(@class,"find")]'           ## Busca
    path2='//div/a[contains(@class,"btn-download")]'       ## Download
 
    print(' ====== Busca')
    driver.find_element(By.XPATH,path).click()
    sleep(2)
    ##print('Anuncio')#sleep(5)#driver.find_elements(By.CLASS_NAME,'btn-close')[0].click()#

    print(" ====== Download ")
    driver.find_element(By.XPATH,path2).click()
    sleep(5)

    #remove arquivo velho
    import os
    for filename in os.listdir(data_path):
        arq = f'SI_{mercado}'
        if arq in filename:
            os.remove(data_path+filename)
    # renomeia arquivo
    dwnld = 'statusinvest-busca-avancada.csv'
    os.rename(data_path+dwnld , data_path+'SI_'+mercado+'.csv')
    driver.close()

           

 
if __name__ == "__main__":

    print(" ====== Status invest ===== ")

    planilha = gc.open('Investimentos')

    for mercado in opcoes_busca.keys() : #['Acoes' ,'Fii' , 'Stocks'] :
        driver = webdriver.Chrome(options=opts) 
        SI(mercado,driver)
        driver.quit()
        print(f" ====== Escrita na planilha {mercado}")

        df = pd.read_csv(data_path+'SI_'+mercado+'.csv', 
                         sep=';' , decimal=',' , header = 0, index_col=False ,  thousands='.' ,
                         encoding='latin1')

        df = df.fillna('')
        #print(df.head(2))

        pagina = planilha.worksheet("StatusInv-"+mercado)
        pagina.clear()
        pagina.update(range_name= 'a2', values= [df.columns.values.tolist()] + df.values.tolist())
        pagina.update(range_name= 'a1',values= [[today]])

        driver.quit()
        print(" ====== Terminou staus invest")

