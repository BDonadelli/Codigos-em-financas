# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 11:17:32 2021

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
import numpy as np

#____________________________________________________________________________________

periods = (100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250)
min_periods_coint = 9
max_critical_value = '5%'

#_______________________________________

symbols = list()
table = pd.DataFrame()

for line in open('C:/Users/danie/.spyder-py3/lista de ativos/IBOV.txt','r').readlines():
    symbols.append(line.strip())
    
mt5.initialize()

for symbol in symbols:
    data = mt5.copy_rates_from(symbol, mt5.TIMEFRAME_D1, datetime.today(), max(periods))
    data = pd.DataFrame(data)
    data['time'] = pd.to_datetime(data['time'], unit='s')
    data.set_index('time', inplace = True)
    table[symbol] = data['close']
    
mt5.shutdown()
    
table.dropna(axis='columns', inplace=True)

pairs = list(permutations(list(table.columns), 2))

table


#_____________________________________________________________________________________

import time
start = time.time()

data = {'Dependente':[], 'Independente':[], 'periodo':[], 'ADF':[], 'Beta':[], 'Desvio':[]}
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
            data1 = {'Dependente':[pair[1]], 'Independente':[pair[0]], 'periodo':[period], 'ADF':[adf], 'Beta':[reg.coef_[0][0]], 'Desvio':[curr_res/std]}
            df2 = pd.DataFrame(data1)
            df1 = df1.append(df2, ignore_index = True)
    
    if len(df1['periodo']) >= min_periods_coint:
        df = df.append(df1, ignore_index = True)
        
        df3 = df.loc[df['Desvio'] > 2]
        df4 = df.loc[df['Desvio'] < -2]
        df5 = df3.append(df4)
        df3 = df.loc[df['Desvio'] > 2]
        df4 = df.loc[df['Desvio'] < -2]
        df5 = df3.append(df4)
        df5["Dependente"] = df5["Dependente"].apply(str)
        df5["Independente"] = df5["Independente"].apply(str)
    
df5["Sinal"] = np.where(df5["Desvio"] >= 2, "Venda " + df5["Independente"] + " Compra " + df5["Dependente"], " Compra " + df5["Independente"] + " Venda " + df5["Dependente"])
df5   



end = time.time()
print(end - start)        
#_____________________________________________________________________________________        
      
df5.to_excel("pairs.xlsx")