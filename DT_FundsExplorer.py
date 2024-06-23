'''
    Esse código baixa planilha de dados do site Funds Explorer
          https://www.fundsexplorer.com.br/ranking
    e grava em um planilha (privada) do google docs
'''

import warnings
warnings.filterwarnings("ignore")

from atualiza_settings import *

def dadosFE (setdriver=True) :

     if setdriver :
          driver=webdriver.Chrome(service=servico, options=opts)
        
     driver.get("https://www.fundsexplorer.com.br/ranking")
     sleep(2)

     print(" ====== Rola pagina")

     # Scroll up the window by a specific number of pixels
     # For example, scroll up by 200 pixels
     scroll_distance = 400
     driver.execute_script(f"window.scrollBy(0, {scroll_distance});")
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

     if setdriver :
          driver.close()

     return df

if __name__ == "__main__":

     df = dadosFE()
     
     print(" ====== Escreve na planilha ====== ")

     planilha = gc.open('Investimentos')
     pagina = planilha.worksheet("FundsExp")
     pagina.clear()

     pagina.update('a1',today)
     pagina.update('a2', [df.columns.values.tolist()] + df.values.tolist())
     # pagina.update('a3',dados)

     print(" ====== Funds Explorer terminou ====== ")

