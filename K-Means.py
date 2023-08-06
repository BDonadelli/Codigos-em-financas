
import numpy as np
import yfinance as yf
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd

import pandas_datareader as dr
from sklearn.cluster import KMeans

# get_ipython().run_line_magic("matplotlib", "inline")
import warnings
warnings.filterwarnings("ignore")


tickers = ['ITSA4.SA' , 'ABCB4.SA' , 'SAPR11.SA', 'CAML3.SA' , 'FLRY3.SA' , 'OFSA3.SA' , 'TAEE11.SA' , 'EGIE3.SA' , 'CXSE3.SA' , 'WIZC3.SA' ,
           'BBAS3.SA' , 'PSSA3.SA',
           'BOAC34.SA' , 'SNEC34.SA' , 'MSFT34.SA' , 'A1MT34.SA' , 'GOGL34.SA', 'KHCB34.SA' , 'COCA34.SA' , 'SPXI11.SA' , 'XINA11.SA' ,
           'AMBP3.SA' , 'MYPK3.SA' ,
           'LVBI11.SA' , 'XPML11.SA' , 'AFHI11.SA' , 'CVBI11.SA' , 'JSRE11.SA' , 'HGRU11.SA' ]

base_ativos = yf.download(tickers, period='3y', auto_adjust=True)['Close']
base_ativos.dropna(inplace=True)

retornos = pd.DataFrame(base_ativos.pct_change().mean()*252)
retornos.columns = ["Retornos"]
retornos["Volatilidade"] = base_ativos.pct_change().std()*np.sqrt(252)

# # # Ajusta os dados para o k-means

x = retornos[["Retornos", "Volatilidade"]]


from yellowbrick.cluster.elbow import kelbow_visualizer
kelbow_visualizer(KMeans(random_state=4), x, k=(2,10)).show()

n_clusters = 4

kmodel = KMeans(n_clusters = n_clusters, random_state = 42)
clusters = kmodel.fit(x)

retornos["Clusters"] = clusters.labels_

cor = ["red" , "blue" , "black" , "purple" , "darkgreen" , 'orange' , "yellow" , "darkblue" , "gray" , "lghtgreen" , "brown" , "olive" , "cyan"]

fig = make_subplots(rows = 1, cols = 1,
                    shared_xaxes = True,
                    vertical_spacing = 0.08)

for i in range(n_clusters) :
  fig.add_trace(go.Scatter(x = retornos.loc[retornos["Clusters"] == i, "Volatilidade"]
                         , y = retornos.loc[retornos["Clusters"] == i, "Retornos"]
                         , name = "Grupo "+str(i), mode = "markers"
                         , text = retornos.loc[retornos["Clusters"] == i].index
                         , marker = dict(size = 16, color = cor[i]))
              , row = 1, col = 1)




fig.update_layout(height = 400, width = 600
                  , title_text = "K-Means clusters"
                  , font_color = "blue"
                  , title_font_color = "black"
                  , xaxis_title = "Retornos"
                  , yaxis_title = "Volatidade"
                  , showlegend = True
                  , legend_title = "Alocação"
                  , font = dict(size = 13, color = "Black")
                 )
fig.update_layout(hovermode = "closest")

fig.show()