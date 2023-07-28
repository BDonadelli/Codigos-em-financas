import pandas as pd
#import datetime as dt
from datetime import datetime


<<<<<<< HEAD
url='https://raw.githubusercontent.com/BDonadelli/Codigos-em-financas/main/feriados.csv'
=======
url = 'https://raw.githubusercontent.com/BDonadelli/Codigos-em-financas/main/feriados.csv'

>>>>>>> baef109a2d6dba0f89948effbc6fec72ab1ecf88
feriado = pd.read_csv(url)
feriado['Data'] =  pd.to_datetime(feriado['Data'], format='%d/%m/%Y')
feriado.set_index(feriado.Data, inplace=True)
#feriado['Data'] = feriado['Data'].astype(str)

print(feriado)

inicio = '2019-01-01'
fim = '2022-12-31'

lista = feriado.Data.loc[inicio:fim].values


print(lista)


for i in range (datetime.strptime(inicio,"%Y-%m-%d") , #
                datetime.strptime(fim,"%Y-%m-%d") ):
    print(i)
