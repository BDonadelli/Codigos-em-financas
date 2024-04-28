
import requests
from bs4 import BeautifulSoup

from datetime import date, timedelta

hoje = date.today()
dia_da_semana = hoje.weekday()  # 0 para segunda-feira, 6 para domingo

if dia_da_semana < 5:  # Se for dia útil (segunda a sexta)
    dia_formatado = hoje.strftime("%d-%m-%Y")
else:  # Se for fim de semana (sábado ou domingo)
    diferenca_dias = dia_da_semana - 4  # Diferença de dias para a sexta-feira
    ultima_sexta = hoje - timedelta(days=diferenca_dias)
    dia_formatado = ultima_sexta.strftime("%d-%m-%Y")

print(dia_formatado)


busca = ''#input('busca por=')


URLs = f'https://entrealtasebaixas.com.br/radar-diario-de-acoes-{dia_formatado}/'


print(URLs)

url=URLs

lista=[]

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
if 'radar-diario-de-acoes' in url : 
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

