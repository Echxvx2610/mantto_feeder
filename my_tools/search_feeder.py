#-*- coding: utf-8 -*-
import csv
import pandas as pd

#configuracion para ver todo un dataframe
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)


data = pd.read_csv(r'PysimpleGUI\Proyectos\mantto_feeder\data\plan feeders SEM.csv',encoding='ISO-8859-1',usecols=['serie','feeder'])
df = pd.DataFrame(data)
df.rename(columns={'serie':'ID_feeder'},inplace=True)
df.rename(columns={'feeder':'Feeder'},inplace=True)

def search_id(ID_FEEDER:int):
    '''
    search_id(ID_FEEDER:int)
    toma como parametro el id del feeder,mismo que sera proporcionado por la app feeder status
    mediante el escaneo de los feeders.
    '''
    #buscar feeder por id
    if ID_FEEDER in df['ID_feeder'].values:
        resultado = df.loc[df['ID_feeder'] == ID_FEEDER].to_string(index = False)
        return resultado
