# -*- coding: utf-8 -*-
'''
Atualiza as informações da planilha 
https://docs.google.com/spreadsheets/d/1hE0ThOaHSg3xdvm12rMSaMvcEFmbko3OcEJ_DwYO3Qo/edit#gid=344141548
'''
import pandas as pd
from datetime import date
today = date.today().strftime('%d/%m/%Y')

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


import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/spreadsheets']
jfile = 'destrincha-fatura.json'

credentials = ServiceAccountCredentials.from_json_keyfile_name(jfile, scope)
gc = gspread.authorize(credentials)


planilha = gc.open('Dados')
pagina=planilha.get_worksheet(1)
pagina.clear()

pagina.update('a1',today)
#pagina.update('a2',td)

print(td)
