busca = input('busca por=')

import requests
from bs4 import BeautifulSoup

URLs = [
        'https://bmcnews.com.br/categoria/analises/', # BMC Analises
        'https://bmcnews.com.br/categoria/economia/', # BMC Economia
        'https://bmcnews.com.br/categoria/mercados/', # BMC Mercados
        'https://bmcnews.com.br/ultimas-noticias/', # BMC ultimas noticias
        'https://comoinvestir.thecap.com.br/t/mercado-financeiro',
        'https://comoinvestir.thecap.com.br/c/noticias',
        'https://comoinvestir.thecap.com.br/c/renda-fixa',
        'https://comoinvestir.thecap.com.br/c/renda-variavel'
        ]

for url in URLs :
  response = requests.get(url)
  soup = BeautifulSoup(response.text, 'html.parser')
  headlines = soup.find('body').find_all('h3')
  for x in headlines:
    if busca in x.text.strip(): print(x.text.strip())

url='https://www.infomoney.com.br/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
headlines = soup.find_all("span", class_="hl-title hl-title-4")
for x in headlines:
    if busca in x.text.strip(): print(x.text.strip())

url='https://www.infomoney.com.br/ultimas-noticias/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
headlines = soup.find_all("span", class_="hl-title hl-title-2")
for x in headlines:
    if busca in x.text.strip(): print(x.text.strip())

url='https://valorinveste.globo.com/ultimas-noticias/'
url='https://valorinveste.globo.com/objetivo/hora-de-investir/'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
headlines = soup.find('body').find_all('h2')
for x in headlines:
  if busca in x.text.strip(): print(x.text.strip())

url='https://financenews.com.br/category/nao-deixe-de-ler/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
headlines = soup.find('body').find_all('h3')
for x in headlines:
  if busca in x.text.strip(): print(x.text.strip())

url='https://financenews.com.br/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
headlines = soup.find('body').find_all('h3')
for x in headlines:
  if busca in x.text.strip(): print(x.text.strip())