
import requests
from bs4 import BeautifulSoup


busca = input('busca por=')


URLs = [
        'https://bmcnews.com.br/categoria/analises/', # BMC Analises
        'https://bmcnews.com.br/categoria/economia/', # BMC Economia
        'https://bmcnews.com.br/categoria/mercados/', # BMC Mercados
        'https://bmcnews.com.br/ultimas-noticias/', # BMC ultimas noticias
        'https://comoinvestir.thecap.com.br/t/mercado-financeiro',
        'https://comoinvestir.thecap.com.br/c/noticias',
        'https://comoinvestir.thecap.com.br/c/renda-fixa',
        'https://comoinvestir.thecap.com.br/c/renda-variavel',
        'https://www.infomoney.com.br/',
        'https://www.infomoney.com.br/ultimas-noticias/',
        'https://valorinveste.globo.com/ultimas-noticias/',
        'https://valorinveste.globo.com/objetivo/hora-de-investir/',
        'https://financenews.com.br/category/nao-deixe-de-ler/',
        'https://financenews.com.br/'
        ]

lista=[]
for url in URLs :
  response = requests.get(url)
  soup = BeautifulSoup(response.text, 'html.parser')
  if 'infomoney' in url : 
    if 'ultimas-noticias' in url : headlines = soup.find_all("span", class_="hl-title hl-title-2")
    else : headlines = soup.find_all("span", class_="hl-title hl-title-4")
  elif 'valorinveste' in url : headlines = soup.find('body').find_all('h2')
  else: headlines = soup.find('body').find_all('h3')
  for x in headlines:
    if busca in x.text.strip() :  
      lista.append(x.text.strip())

noticias = list(set(lista))
print(noticias)