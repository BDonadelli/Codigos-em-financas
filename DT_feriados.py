import pandas as pd
#import datetime as dt
from datetime import datetime

def feriados(inicio:datetime , fim:datetime): 

    url='https://raw.githubusercontent.com/BDonadelli/Codigos-em-financas/main/data/feriados.csv'
    feriado = pd.read_csv(url)
    feriado['Data'] =  pd.to_datetime(feriado['Data'], format='%d/%m/%Y')
    feriado.set_index(feriado.Data, inplace=True)
    #feriado['Data'] = feriado['Data'].astype(str)

    lista = feriado.Data.loc[inicio:fim].values

    return(lista)


if __name__ == "__main__":


    inicio =datetime(2024,9,1)
    fim = datetime(2024,12,2)

    print(feriados(inicio,fim))
    
