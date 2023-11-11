codigo  

inicio

termino

usar_periodo = False #@param {type:"boolean"}

periodo = '2y' #@param ['1d','5d','1mo','3mo','6mo','1y','2y','3y','5y','10y','ytd','max']

quandlkey = 'XjVtHyrCSxB4xG9iyLUx'

IBr50 *carteira teorica ou setor de 'codigo'*

k_info, info, L52, H52, HP, LP, MP, mP, rec, nAnal *infos do yfinanace*

funds, dfunds *pandas do fundamentus*

ativo = pd.DataFrame() *preços do ativo* codigo

ibov = pd.DataFrame() *preços do ibov*

provento, yanual *dividendos*

preco *preços do ativo (+bollinger) e ibov* 

n_dias, n_grafico, n_cenarioss_media, s_variancia, s_desvio_padrao, Z , retornos_diarios, previsoes, cenarios *\## simula movimento browniano geométrico (MBG)*

IBr50_preco



uem gosta muito de operações assim é o Fernando roxo né ele ele costuma montar
21:32
operações dessa forma com a venda que de qual ou de Putz comprando Putz mais
21:39
baratas né Putz no pozinho né que ele é muito famoso por isso para poder fazer isso daqui na teoria funciona muito bems na prática a gente vê que não é bem assim e funciona eu posso voltar para o nosso gráfico aqui e aí a gente tem que
