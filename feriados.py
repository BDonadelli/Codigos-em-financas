import pandas as pd

feriado = pd.read_csv('feriados.csv')
feriado['Data'] =  pd.to_datetime(feriado['Data'], format='%d/%m/%Y')
feriado.set_index(feriado.Data, inplace=True)
feriado['Data'] = feriado['Data'].astype(str)

inicio = '2019-01-01'
fim = '2022-12-31'

lista = feriado.Data.loc[inicio:fim].values


print( lista)

