import numpy as np
import pandas as pd

import yfinance as yf

import matplotlib.pyplot as plt
import plotly.graph_objects as go

symbol = input('ticker=')+'.SA'
periodo = str( input('1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max. :'))

tickers = yf.Ticker(symbol)
df = tickers.history(period=periodo)
df["Date"]=df.index

# feriados

inicio = df.index[0].strftime("%Y-%m-%d")
fim = df.index[-1].strftime("%Y-%m-%d")

feriado = pd.read_csv('data/feriados.csv')
feriado['Data'] =  pd.to_datetime(feriado['Data'], format='%d/%m/%Y')
feriado.set_index(feriado.Data, inplace=True)
feriado['Data'] = feriado['Data'].astype(str)

lista = feriado.Data.loc[inicio:fim].values

# feriados

print(lista)

# calcular a média de 30 dias
avg_5 = df.Close.rolling(window=9, min_periods=1).mean()
avg_20 = df.Close.rolling(window=21, min_periods=1).mean()
avg_60 = df.Close.rolling(window=72, min_periods=1).mean()
avg_200 = df.Close.rolling(window=250, min_periods=1).mean()


trace1 = { 'x': df.Date,
           'open': df.Open,
           'close': df.Close,
           'high': df.High,
           'low': df.Low,
           'type': 'candlestick',
           'name': symbol,
           'showlegend': True }
# média de 20 dias (linha)
trace2 = { 'x': df.Date,
           'y': avg_20,
           'type': 'scatter',
           'mode': 'lines',
           'line': {'width': 1,'color': 'orange'},
           'name': 'Média (21 dias)' }
trace3 = { 'x': df.Date,
           'y': avg_60,
           'type': 'scatter',
           'mode': 'lines',
           'line': { 'width': 1,'color': 'red'},
           'name': 'Média (72 dias)'}
trace4 = { 'x': df.Date,
           'y': avg_5,
           'type': 'scatter',
           'mode': 'lines',
           'line': {'width': 1, 'color': 'blue' },
           'name': 'Média (09 dias)'}
trace5 = { 'x': df.Date,
           'y': avg_200,
           'type': 'scatter',
           'mode': 'lines',
           'line': {'width': 1,'color': 'brown'},
            'name': 'Média (250 dias)'}
# informar todos os dados e gráficos em uma lista
data = [trace4,trace1,trace2,trace3,trace5]
 
# configurar o layout do gráfico
layout = go.Layout({ 'title': {'text': 'Gráfico de Candlestick','font': {  'size': 10   }  }})
 
# instanciar objeto Figure e plotar o gráfico
fig = go.Figure(data=data, layout=layout)


fig.update_xaxes(
        rangeslider_visible=True,
        rangebreaks=[
            # NOTE: Below values are bound (not single values), ie. hide x to y
            dict(bounds=["sat", "mon"]),  # hide weekends, eg. hide sat to before mon
            #dict(bounds=[16, 9.5], pattern="hour"),  # hide hours outside of 9.30am-4pm
            dict(values=lista)#["2018-12-24","2019-12-24", "2020-12-24", "2021-12-24", "2022-12-24"]) ,
            #dict(values=["2018-12-25","2019-12-25", "2020-12-25", "2021-12-24", "2022-12-24"]) ,
            #dict(values=["2018-01-01","2019-01-01", "2020-01-01", "2021-01-01", "2022-01-01"])
        ]
    )

fig.show()

