import numpy as np
import pandas as pd
from pandas_datareader import data as web
import yfinance as yf
import matplotlib.pyplot as plt
import plotly.graph_objects as go

acoes = ['WEGE3.SA' , 'ITSA4.SA' , 'MGLU3.SA', '^BVSP']
inicio = '2019-04-29'
df = yf.download(acoes[3])
df["Date"]=df.index

# calcular a média de 30 dias
avg_20 = df.Close.rolling(window=21, min_periods=1).mean()
avg_60 = df.Close.rolling(window=60, min_periods=1).mean()

trace1 = {
    'x': df.Date,
    'open': df.Open,
    'close': df.Close,
    'high': df.High,
    'low': df.Low,
    'type': 'candlestick',
    'name': 'ITSA',
    'showlegend': False
}
# média de 20 dias (linha)
trace2 = {
    'x': df.Date,
    'y': avg_20,
    'type': 'scatter',
    'mode': 'lines',
    'line': {
        'width': 1,
        'color': 'blue'
    },
    'name': 'Média (20 dias)'
}
trace3 = {
    'x': df.Date,
    'y': avg_60,
    'type': 'scatter',
    'mode': 'lines',
    'line': {
        'width': 1,
        'color': 'red'
    },
    'name': 'Média (60 dias)'
}


# informar todos os dados e gráficos em uma lista
data = [trace1,trace2,trace3]
 
# configurar o layout do gráfico
layout = go.Layout({
    'title': {
        'text': 'Gráfico de Candlestick',
        'font': {
            'size': 10
        }
    }
})
 
# instanciar objeto Figure e plotar o gráfico
fig = go.Figure(data=data, layout=layout)
fig.show()
