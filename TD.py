from urllib.request import urlopen
  
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import json

url = 'https://www.tesourodireto.com.br/json/br/com/b3/tesourodireto/service/api/treasurybondsinfo.json'
  
response = urlopen(url)
  
data_json = json.loads(response.read())
  
data_json['response']