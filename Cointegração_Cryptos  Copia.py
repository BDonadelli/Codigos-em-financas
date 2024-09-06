# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 10:34:58 2021

@author: Home
"""

import math
import statistics
from datetime import datetime, time
from itertools import permutations
import pandas as pd
import MetaTrader5 as mt5
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from sklearn.linear_model import LinearRegression
from binance.client import Client
import pandas as pd
import numpy as np
from datetime import datetime
import time
#start = time.time()
key = ''
secret = ''
client = Client(api_key = key, api_secret = secret)
c = Client()


periods = (100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250)
min_periods_coint = 9
max_critical_value = '5%'


coins = []
symbols = list()
df = pd.DataFrame()
table = pd.DataFrame()

for line in open('C:/Users/danie/.spyder-py3/lista de ativos/cryptos.txt','r').readlines():
    symbols.append(line.strip())
            
df = pd.DataFrame(symbols, columns=['coin'])
df.head()

# Obtains data for a specified symbol, interval and limit
# Can be modified by adding start and end dates
def GetData (symbol, interval, limit):
    data = c.get_klines(symbol=symbol, interval=interval, limit=limit)
    x = 0
    full = {}

    for k in data:
        #print(k)
        j = []
        x += 1
        for i in k[:5]:
            j.append(float(i))
        dat = pd.DataFrame(j).T
        full[str(x)] = dat

    df = pd.concat(full)
    df.reset_index(drop=True, inplace=True)
    df.columns = ['date','open','high','low','close']
    df['date'] = pd.to_datetime(df['date'], unit='ms')
    df = df.assign(symbols=symbol)
    return(df)


historical = pd.DataFrame()
hist = {}

for i in symbols:
    coin_hist = GetData(symbol=i, interval='1d', limit=250)
    hist[i] = coin_hist
#hist


data = pd.concat(hist)
data.reset_index(drop=True, inplace=True)

df = data.pivot(index='date', columns='symbols', values='close')

df.dropna(axis='columns', inplace=True)

mod = df.reset_index()

mod.set_index('date', inplace = True)
for d in symbols:
    table[d] = mod[d]


pairs = list(permutations(list(df.columns), 2))

table

data = {'Independente':[], 'Dependente':[], 'periodo':[], 'ADF':[], 'Beta':[], 'Desvio':[]}
df = pd.DataFrame(data)
for pair in pairs:
    df1 = pd.DataFrame(data)
    for period in periods:
        
        x = table[pair[0]].tail(period).values.reshape(-1, 1)
        y = table[pair[1]].tail(period).values.reshape(-1, 1)
        
        reg = LinearRegression().fit(x, y)
        pred = reg.predict(x)
        res = y - pred
        adf, pvalue, usedlag, nobs, critical_values, icbest = adfuller(res)
        
        r1 = [i[0] for i in res]
        curr_res = r1[-1:][0]
        std = statistics.stdev(r1)
        
        if adf < critical_values[max_critical_value]:
            data1 = {'Independente':[pair[0]], 'Dependente':[pair[1]], 'periodo':[  period], 'ADF':[adf], 'Beta':[reg.coef_[0][0]], 'Desvio':[curr_res/std]}
            df2 = pd.DataFrame(data1)
            df1 = df1.append(df2, ignore_index = True)
    
    if len(df1['periodo']) >= min_periods_coint:
        df = df.append(df1, ignore_index = True)       
        
        df3 = df.loc[df['Desvio'] > 2]
        df4 = df.loc[df['Desvio'] < -2]
        df5 = df3.append(df4)
        df5["Dependente"] = df5["Dependente"].apply(str)
        df5["Independente"] = df5["Independente"].apply(str)
    
df5["Sinal"] = np.where(df5["Desvio"] >= 2, "Venda " + df5["Independente"] + " Compra " + df5["Dependente"], " Compra " + df5["Independente"] + " Venda " + df5["Dependente"])
end = time.time()
#print(end - start)
df5    



