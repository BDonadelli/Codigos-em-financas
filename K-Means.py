
import numpy as np
import yfinance as yf
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas_datareader as dr
from math import sqrt
from sklearn.cluster import KMeans

get_ipython().run_line_magic("matplotlib", "inline")
import warnings
warnings.filterwarnings("ignore")


tickers = ["^BVSP", "BRL=X", "BOVA11.SA", "PETR4.SA", "VALE", "ITUB4.SA"
           , "CSNA3.SA", "BBAS3.SA", "WEGE3.SA", "B3SA3.SA" ,  "JBSS3.SA"
           , "ITSA4.SA", "CMIG4SA", "SBSP3.SA", "CCRO3.SA", "UGPA3.SA"
           , "MULT3.SA", "MGLU3.SA", "EQTL3.SA", "LREN3.SA", "ENBR3.SA"
           ,"ABEV3.SA", "SUZB3.SA", "^GSPC", "BTC-USD", "ETH-USD"
           , "GBPUSD=X", "EURUSD=X", "^VIX"]

ativos = []
for ticker in tickers:
    try:
        cotacoes = dr.DataReader(ticker, "yahoo", "01/01/2017")["Adj Close"]
        cotacoes = pd.DataFrame(cotacoes)
        cotacoes.columns = [ticker]
        ativos.append(cotacoes)
    except:
        pass
    base_ativos = pd.concat(ativos, axis = 1)
base_ativos.sort_index(inplace = True)
base_ativos.head()


# In[4]:


# Vamos criar e agrupar as informações com base anual média

retornos = pd.DataFrame(base_ativos.pct_change().mean()*252)
retornos.columns = ["Retornos"]
retornos["Volatilidade"] = base_ativos.pct_change().std()*sqrt(252)

# Ajusta os dados para o k-means

x = retornos[["Retornos", "Volatilidade"]]
min_clusters = 2
max_clusters = 10
inertias = np.zeros(shape = (max_clusters - min_clusters + 1,))

for i in range(min_clusters, max_clusters + 1):
    kmeans = KMeans(n_clusters = i, random_state = 42)
    kmeans.fit(x)
    inertias[i - min_clusters] = kmeans.inertia_


# In[5]:


# Gráfico do método do cotovelo

fig = make_subplots(rows = 1, cols = 1,
                    shared_xaxes = True,
                    vertical_spacing = 0.08)

fig.add_trace(go.Scatter(x = list(range(2,10)), y = inertias
                         , name = "Inertia", line = dict(color = "blue"))
              , row = 1, col = 1)


fig.update_layout(height = 400, width = 600
                  , title_text = "Determinação do # de clusters - Método do cotovelo"
                  , font_color = "blue"
                  , title_font_color = "black"
                  , xaxis_title = "Número de Clusters"
                  , yaxis_title = "Inertia"
                  , legend_title = "Study objects"
                  , font = dict(size = 15, color = "Black")
                 )
fig.update_layout(hovermode = "x")

fig.show()


# In[6]:


# Ajuste do K-Means

kmodel = KMeans(n_clusters = 5, random_state = 42)
clusters = kmodel.fit(x)


# In[7]:


# Acessando os clusters

clusters.labels_


# In[8]:


retornos["Clusters"] = clusters.labels_


# In[9]:


retornos


# In[10]:


# Avaliação dos resultados - 2 métodos de construir o gráfico
# Método 1

fig = make_subplots(rows = 1, cols = 1,
                    shared_xaxes = True,
                    vertical_spacing = 0.08)

fig.add_trace(go.Scatter(x = retornos.loc[retornos["Clusters"] == 0, "Volatilidade"]
                         , y = retornos.loc[retornos["Clusters"] == 0, "Retornos"]
                         , name = "Grupo 1", mode = "markers"
                         , text = retornos.loc[retornos["Clusters"] == 0].index
                         , marker = dict(size = 16, color = "red"))
              , row = 1, col = 1)

fig.add_trace(go.Scatter(x = retornos.loc[retornos["Clusters"] == 1, "Volatilidade"]
                         , y = retornos.loc[retornos["Clusters"] == 1, "Retornos"]
                         , name = "Grupo 2", mode = "markers"
                         , text = retornos.loc[retornos["Clusters"] == 1].index
                         , marker = dict(size = 16, color = "blue"))
              , row = 1, col = 1)

fig.add_trace(go.Scatter(x = retornos.loc[retornos["Clusters"] == 2, "Volatilidade"]
                         , y = retornos.loc[retornos["Clusters"] == 2, "Retornos"]
                         , name = "Grupo 3", mode = "markers"
                         , text = retornos.loc[retornos["Clusters"] == 2].index
                         , marker = dict(size = 16, color = "black"))
              , row = 1, col = 1)

fig.add_trace(go.Scatter(x = retornos.loc[retornos["Clusters"] == 3, "Volatilidade"]
                         , y = retornos.loc[retornos["Clusters"] == 3, "Retornos"]
                         , name = "Grupo 4", mode = "markers"
                         , text = retornos.loc[retornos["Clusters"] == 3].index
                         , marker = dict(size = 16, color = "purple"))
              , row = 1, col = 1)

fig.add_trace(go.Scatter(x = retornos.loc[retornos["Clusters"] == 4, "Volatilidade"]
                         , y = retornos.loc[retornos["Clusters"] == 4, "Retornos"]
                         , name = "Grupo 5", mode = "markers"
                         , text = retornos.loc[retornos["Clusters"] == 4].index
                         , marker = dict(size = 16, color = "darkgreen"))
              , row = 1, col = 1)


fig.update_layout(height = 400, width = 600
                  , title_text = "K-Means para seleção de ativos - www.outspokenmarket.com"
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


# In[11]:


# Avaliação dos resultados - 2 métodos de construir o gráfico
# Método 2

fig = make_subplots(rows = 1, cols = 1,
                    shared_xaxes = True,
                    vertical_spacing = 0.08)

fig.add_trace(go.Scatter(x = retornos["Volatilidade"], y = retornos["Retornos"]
                         , name = "", mode = "markers"
                         , text = retornos.index
                         , marker = dict(size = 16, color = retornos["Clusters"]))
              , row = 1, col = 1)


fig.update_layout(height = 400, width = 600
                  , title_text = "K-Means para seleção de ativos - www.outspokenmarket.com"
                  , font_color = "blue"
                  , title_font_color = "black"
                  , xaxis_title = "Retornos"
                  , yaxis_title = "Volatidade"
                  , showlegend = False
                  , legend_title = "Alocação"
                  , font = dict(size = 13, color = "Black")
                 )
fig.update_layout(hovermode = "closest")

fig.show()

