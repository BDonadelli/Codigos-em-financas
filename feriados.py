import pandas as pd
#import datetime as dt
from datetime import datetime


url='https://raw.githubusercontent.com/BDonadelli/Codigos-em-financas/main/feriados.csv'
feriado = pd.read_csv(url)
feriado['Data'] =  pd.to_datetime(feriado['Data'], format='%d/%m/%Y')
feriado.set_index(feriado.Data, inplace=True)
#feriado['Data'] = feriado['Data'].astype(str)

inicio = '2019-01-01'
fim = '2022-12-31'

lista = feriado.Data.loc[inicio:fim].values


print(lista)


for i in range (datetime.strptime(inicio,"%Y-%m-%d") , #
                datetime.strptime(fim,"%Y-%m-%d") ):
    print(i)
