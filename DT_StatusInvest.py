from  atualiza_settings import *

opcoes_busca = {'Acoes': 'acoes' , 'Fii':'fundos-imobiliarios' , 'Stocks':'acoes/eua'}


def SI(mercado = 'Acoes' , setdriver=True ) :

    print(f" ====== SI {mercado} ===== ")

    if setdriver :
        driver=webdriver.Chrome(service=servico, options=opts)

    onde = opcoes_busca[mercado]
    url = f'https://statusinvest.com.br/{onde}/busca-avancada'

    driver.get(url)
    sleep(3)

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
            
    if setdriver :
        driver.close()

 
if __name__ == "__main__":

    print(" ====== Status invest ===== ")

    planilha = gc.open('Investimentos')

    for mercado in opcoes_busca.keys() : #['Acoes' ,'Fii' , 'Stocks'] :
        SI(mercado, True)

        print(f" ====== Escrita na planilha {mercado}")

        df = pd.read_csv(data_path+'SI_'+mercado+'.csv', 
                         sep=';' , decimal=',' , header = 0, index_col=False ,  thousands='.' ,
                         encoding='latin1')

        df = df.fillna('')
        #print(df.head(2))

        pagina = planilha.worksheet("StatusInv-"+mercado)
        pagina.clear()
        pagina.update('a2', [df.columns.values.tolist()] + df.values.tolist())
        pagina.update('a1',today)

print(" ====== Terminou staus invest")

