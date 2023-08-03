import pandas as pd

from urllib.request import urlopen

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import json
url = 'https://www.tesourodireto.com.br/json/br/com/b3/tesourodireto/service/api/treasurybondsinfo.json'
response = urlopen(url)
data_json = json.loads(response.read())

nome , pr , pc , tr , tc = [],[],[],[],[]
td=pd.DataFrame()

for i in range(len(data_json["response"]["TrsrBdTradgList"])):
  nome.append(data_json["response"]["TrsrBdTradgList"][i]['TrsrBd']['nm'])
  pr.append(data_json["response"]["TrsrBdTradgList"][i]['TrsrBd']['untrRedVal'])
  pc.append(data_json["response"]["TrsrBdTradgList"][i]['TrsrBd']['untrInvstmtVal'])
  tr.append(data_json["response"]["TrsrBdTradgList"][i]['TrsrBd']['anulRedRate'])
  tc.append(data_json["response"]["TrsrBdTradgList"][i]['TrsrBd']['anulInvstmtRate'])

td['título'] = nome
td['preço resgate'] = pr
td['preço compra'] = pc
td['taxa resgate'] = tr
td['taxa compra'] = tc

td=td.fillna("")

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/spreadsheets']
jfile = 'carteira-328314-d38dcc8ee3e4.json'

credentials = ServiceAccountCredentials.from_json_keyfile_name(jfile, scope)
gc = gspread.authorize(credentials)

planilha = gc.open('Dados')
pagina = planilha.worksheet("Tesouro Direto")

# #pagina.clear()
pagina.update('e1',td)

# # registra data da ultima atualização
# from datetime import date
# today = date.today().strftime('%d/%m/%Y')
# pagina.update('h1',today)