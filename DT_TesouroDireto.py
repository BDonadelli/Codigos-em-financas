from atualiza_settings import *


def dadosTD() :

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

  td['Ano'] = td['título'].str.extract(r'\b(\d{4})\b')
  td = td.sort_values(by=['título','Ano'], ascending=True)
  td.drop(['Ano'],axis=1,inplace=True)

  meus_tits = []
  for linha in range(3,11):
    meus_tits.append(pagina.cell(linha, 1).value)

  meus = td[td['título'].isin(meus_tits)].copy()
  meus['título']= meus['título'].str.replace('Tesouro ', '')
  meus['título']= meus['título'].str.replace('com Juros Semestrais', 'Juros')
  meus['título']= meus['título'].str.replace('20', '')
  meus = meus.rename(columns={'título':str(today)})

  return td, meus

if __name__ == "__main__":

  print(" ====== Tesouro Direto  ===== ")
  
  td, meus = dadosTD()

  print(" ====== Escreve na planilha")

  planilha = gc.open('Investimentos')
  pagina = planilha.worksheet('Renda Fixa')

  from waitinput import input_with_timeout
  linha = int(input_with_timeout('linha da celula inicial (74)', 5, 74))

  pagina.update_cell(linha, 1,  today )
  pagina.update('a'+str(linha+1),[td.columns.values.tolist()] + td.values.tolist())

  pagina.update_cell(2, 12,  today )
  pagina.update('l2',[meus.columns.values.tolist()] + meus.values.tolist())

  print(" ====== Tesouro Direto terminou")
