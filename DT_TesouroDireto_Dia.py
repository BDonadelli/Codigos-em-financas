
'''
versão de DT_TesouroDireto_Dia_planilha_v2.ipynb
para executar no terminal, atualiza 'tesouro_direto.json' 
'''
url = 'https://www.tesourodireto.com.br/json/br/com/b3/tesourodireto/service/api/treasurybondsinfo.json'
from selenium import webdriver
driver=webdriver.Chrome()
driver.get(url)
page_source = driver.page_source
start = page_source.find("{")
end = page_source.rfind("}") + 1
json_text = page_source[start:end]
import json
data_json = json.loads(json_text)
driver.close()
with open('data/tesouro_direto.json', 'w', encoding='utf-8') as json_file:
    json.dump(data_json, json_file, ensure_ascii=False, indent=4)
import git  # atualiza repositorio github
repo = git.Repo('.')
repo.git.add(A=True)
repo.index.commit("Atualiza 'data/tesouro_direto.json'")
origin = repo.remote(name='origin')
origin.push()