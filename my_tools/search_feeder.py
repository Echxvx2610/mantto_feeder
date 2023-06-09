#-*- coding: utf-8 -*-
import csv
import pandas as pd

#configuracion para ver todo un dataframe
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)


data = pd.read_csv(r'PysimpleGUI\Proyectos\mantto_feeder\data\plan feeders SEM.csv',encoding='ISO-8859-1',usecols=['serie','feeder'])
df = pd.DataFrame(data)

def search_id(ID_FEEDER:int):
    '''
    search_id(ID_FEEDER:int)
    toma como parametro el id del feeder,mismo que sera proporcionado por la app feeder status
    mediante el escaneo de los feeders.
    '''
    #buscar feeder por id
    if ID_FEEDER in df['serie'].values:
        resultado = df.loc[df['serie'] == ID_FEEDER].to_string(index = False)
        print(resultado)
    else:
        print('no existe')
    
    

#search_id(104554705)

