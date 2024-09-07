'''
    Esse código baixa planilha de dados do site Fundamentus
        https://www.fundamentus.com.br/resultado.php
    e grava em um planilha (privada) do google docs
'''
import warnings
warnings.filterwarnings("ignore")
from DT_atualiza_settings import *

def dadosFund () :
    import requests
    url1 = 'https://www.fundamentus.com.br/resultado.php'
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    r1 = requests.get(url1, headers=header)
    return pd.read_html(r1.text, decimal=',', thousands='.')[0]
    
if __name__ == "__main__":

    dfs = dadosFund ()
    print(" ====== Escreve na planilha  ====== ")
    planilha = gc.open('Investimentos')
    pagina = planilha.worksheet("Fundamentus")
    pagina.clear()
    pagina.update(range_name='a2', values=[dfs.columns.values.tolist()] + dfs.values.tolist())
    pagina.update(range_name='a1',values=[[date.today().strftime('%d/%m/%Y')]])
    print(" ====== Terminou ======")

