from DT_atualiza_settings import *

def dadosFE (setdriver=False) :

     if setdriver :
          driver=webdriver.Chrome(options=opts)
        
     driver.get("https://www.fundsexplorer.com.br/ranking")
     sleep(2)
     fecha_prop_path='//*[@id="hs-eu-confirmation-button"]'
     driver.find_element(By.XPATH,fecha_prop_path).click()
     sleep(2)

#-------------# Muda o contexto para o iframe 
     iframe_element = driver.find_element(By.XPATH, "//iframe[@title='Popup CTA']")
     driver.switch_to.frame(iframe_element)
# Encontra o botão "X" dentro do iframe
     close_button = driver.find_element(By.XPATH, "/html/body/div/div[1]")
# Clique no botão "X"
     close_button.click()
# Volte para o contexto principal
     driver.switch_to.default_content()
#------------------------------------

     print(" ====== Rola pagina")

     # Scroll up the window by a specific number of pixels
     # For example, scroll up by 200 pixels
     scroll_distance = 500
     # print('111')
     driver.execute_script(f"window.scrollBy(0, {scroll_distance});")
     # print('222')
     sleep(2)
     
     print(" ====== Escolhe todas as colunas ")
     
     driver.find_element(By.XPATH,'//*[@id="colunas-ranking__select-button"]').click()
     sleep(2)
     driver.find_element(By.XPATH,'/html/body/div[7]/div[1]/div/div[2]/div[2]/ul/li[1]/label').click()
     sleep(2)
     
     print(" ====== lê a tabela ")
     
     dados = []
     dadosTabela = driver.find_element(By.XPATH,'//div/table[contains(@class,"default-fiis-table__container__table")]')
     
     #print(dadosTabela.text)  

     for linha in dadosTabela.find_elements(By.TAG_NAME,"tr") :
         linhaDados = []
         for coluna in linha.find_elements(By.TAG_NAME,"td"):
              # print(coluna)
              linhaDados.append(coluna.text)
         dados.append(linhaDados)

     print(" ====== monta dataframe ====== ")

     colunas = ['Fundos','Setor','Preço Atual (R$)','Liquidez Diária (R$)',#
          'P/VP','Último Dividendo','Dividend Yield','DY (3M) Acumulado',#
          'DY (6M) Acumulado','DY (12M) Acumulado','DY (3M) média','DY (6M) média',#
          'DY (12M) média','DY Ano','Variação Preço','Rentab. Período','Rentab. Acumulada',#
          'Patrimônio Líquido','VPA','P/VPA','DY Patrimonial','Variação Patrimonial',#
          'Rentab. Patr. Período','Rentab. Patr. Acumulada','Quant. Ativos' ,'Volatilidade' , #
          'Num. Cotistas' , 'Tax. Gestão' , 'Tax. Performance' , 'Tax. Administração']

     df = pd.DataFrame(dados,columns=colunas)

     driver.close()

     return df

def dadosInfra (setdriver=False) :

    if setdriver :
        driver=webdriver.Chrome(options=opts)
    
    xpath1='//*[@id="table-indicators"]/div[12]/div[2]/div/span'
    xpath2='//*[@id="table-indicators"]/div[14]/div[2]/div'
    xpath3='//*[@id="cards-ticker"]/div[2]/div[2]/div/span'

    print(" ======  JURO11 ")

    # driver.get("https://data.anbima.com.br/fundos/627127")
    driver.get("https://investidor10.com.br/fiis/juro11/")

    sleep(3)

    juro11_vpa = driver.find_element(By.XPATH,xpath1).text
    juro11_div = driver.find_element(By.XPATH,xpath2).text
    juro11_dy = driver.find_element(By.XPATH,xpath3).text

    print(" ======  BIDB11 ")

    # driver.get("https://data.anbima.com.br/fundos/617350")
    driver.get("https://investidor10.com.br/fiis/bidb11/")
    sleep(3)

    bidb11_vpa = driver.find_element(By.XPATH,xpath1).text
    bidb11_div = driver.find_element(By.XPATH,xpath2).text
    bidb11_dy = driver.find_element(By.XPATH,xpath3).text

    print(" ======  CPTI11 ")

    # driver.get("https://data.anbima.com.br/fundos/617350")
    driver.get("https://investidor10.com.br/fiis/cpti11/")
    sleep(3)

    cpti11_vpa = driver.find_element(By.XPATH,xpath1).text
    cpti11_div = driver.find_element(By.XPATH,xpath2).text
    cpti11_dy = driver.find_element(By.XPATH,xpath3).text

    driver.close()

    return juro11_vpa,juro11_div,juro11_dy,bidb11_vpa, bidb11_div, bidb11_dy ,cpti11_vpa , cpti11_div , cpti11_dy



if __name__ == "__main__":

     try: 
          driver.close()
     except:
          pass      


     print(" ====== Funds Explorer ===== ")

     df = dadosFE(True)
     
     print(" ====== Escreve na planilha")

     planilha = gc.open('Investimentos')
     pagina = planilha.worksheet("FundsExp")
     pagina.clear()

     pagina.update(range_name= 'a1',values= [[today]])
     pagina.update(range_name=  'a2',values=  [df.columns.values.tolist()] + df.values.tolist())
     # pagina.update('a3',dados)

     print(" ====== Funds Explorer terminou")

     print(" ====== FI-Infra ===== ")

     juro11_vpa,juro11_div,juro11_dy,bidb11_vpa, bidb11_div, bidb11_dy ,cpti11_vpa , cpti11_div , cpti11_dy = dadosInfra(True)


     print(" ====== Escreve na planilha")

     planilha = gc.open('Investimentos')
     pagina = planilha.worksheet('FundsExp')
       
     pagina.update(range_name='b1',values= [["juro11 (VPA,Prov,DY)"]])
     pagina.update(range_name='c1',values= [[juro11_vpa]])
     pagina.update(range_name='d1',values= [[juro11_div]])
     pagina.update(range_name='e1',values= [[juro11_dy]])
     pagina.update(range_name='f1',values= [["bidb11 (VPA,Prov,DY)"]])
     pagina.update(range_name='g1',values= [[bidb11_vpa]])
     pagina.update(range_name='h1',values= [[bidb11_div]])
     pagina.update(range_name='i1',values= [[bidb11_dy]])
     pagina.update(range_name='j1',values= [["cpti11 (VPA,Prov,DY)"]])
     pagina.update(range_name='k1',values= [[cpti11_vpa]])
     pagina.update(range_name='l1',values= [[cpti11_div]])
     pagina.update(range_name='m1',values= [[cpti11_dy]])

     print(" ====== FI-Infra Terminou")





