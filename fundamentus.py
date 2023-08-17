import requests
import pandas as pd



url1 = 'https://www.fundamentus.com.br/resultado.php'
#ptra fingir que é um browser
header = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}
#junta com a requests
r1 = requests.get(url1, headers=header)
# read_html do pandas põe a tabela num dataframe
dfs = pd.read_html(r1.text, decimal=',', thousands='.')[0]

print(dfs)

import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = ['https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/spreadsheets']
jfile = 'carteira-328314-d38dcc8ee3e4.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(jfile, scope)
gc = gspread.authorize(credentials)

planilha = gc.open('Investimentos')
pagina = planilha.worksheet("Fundamentus")

pagina.clear()

pagina.update('a2', [dfs.columns.values.tolist()] + dfs.values.tolist())
# # registra data da ultima atualização
from datetime import date
pagina.update('a1',date.today().strftime('%d/%m/%Y'))