
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions, Chrome, Keys


import pandas as pd
import sys,csv
import numpy as np

filename = 'fluxo-historico.csv'
with open(filename, "r") as f:
  reader = csv.reader(f, delimiter=',')
  x=list(reader)

a=[]
ind=[]
for l in range(1,len(x)):
  ind.append(x[l][0])
  i=1
  while i < 11 :      
      a.append(x[l][i].replace('.','')+'.'+x[l][i+1][:-3])
      i=i+2

data = np.array( a,dtype=float )
m=data.reshape( len(x)-1 , 5 )
df = pd.DataFrame(m, index=ind  , columns=x[0][1:])
print(df.tail())

import plotly.graph_objects as go

fig = go.Figure(go.Bar(
            x=df.index[::-1] , 
            y=df.Estrangeiro[::-1] ,
            orientation='v'))

fig.show()