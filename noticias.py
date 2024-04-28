
import requests
from bs4 import BeautifulSoup
import re
from datetime import date, timedelta

hoje = date.today()
dia_da_semana = hoje.weekday()  # 0 para segunda-feira, 6 para domingo

if dia_da_semana < 5:  # Se for dia útil (segunda a sexta)
    dia_formatado = hoje.strftime("%d-%m-%Y")
else:  # Se for fim de semana (sábado ou domingo)
    diferenca_dias = dia_da_semana - 4  # Diferença de dias para a sexta-feira
    ultima_sexta = hoje - timedelta(days=diferenca_dias)
    dia_formatado = ultima_sexta.strftime("%d-%m-%Y")


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
        'https://financenews.com.br/',
        'https://entrealtasebaixas.com.br/', 
        #o proximo fica por ultimo
        f'https://entrealtasebaixas.com.br/radar-diario-de-acoes-{dia_formatado}/'
        ]

lista=[]
for url in URLs :
  response = requests.get(url)
  soup = BeautifulSoup(response.text, 'html.parser')

  if 'radar-diario-de-acoes' not in url :    
    if 'infomoney' in url : 
      if 'ultimas-noticias' in url : headlines = soup.find_all("span", class_="hl-title hl-title-2")
      else : headlines = soup.find_all("span", class_="hl-title hl-title-4")
    elif 'valorinveste' in url : headlines = soup.find('body').find_all('h2')
    else: headlines = soup.find('body').find_all('h3')
    for x in headlines:
      if busca in x.text.strip() :  
        lista.append(x.text.strip())

    noticias = list(set(lista))
    print(*noticias,sep='\n')


print('Destaques de hoje')

codigos = soup.find_all("strong")
# print(codigos)

for codigo in codigos:
    # print(codigo)
    if codigo.text.strip() != 'Entrealtasebaixas.com.br':
          
      # Extrai o texto do elemento 'strong' (por exemplo, 'BRSR6')
      codigo_texto = codigo.text.strip()
      # print(codigo_texto)

      import re
      texto_apos_strong = re.search(r"</strong>(.*)", str(codigo.parent)).group(1).strip()
      # print(texto_apos_strong)

      print(f"\n{codigo_texto} {texto_apos_strong}")
      print()
