#-*- coding: utf-8 -*-
import csv
import pandas as pd
import openpyxl
from openpyxl import workbook,load_workbook
from openpyxl.utils import get_column_letter

#*********************** Configuracion de dataframe(muestra todo el dataframe)********************
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)

#***************************** Creacion de un dataframe ********************************
data = pd.read_csv(r'PysimpleGUI\Proyectos\mantto_feeder\data\plan feeders SEM.csv',encoding='ISO-8859-1',usecols=['serie','feeder'])
df = pd.DataFrame(data)
#**************************** Renombrar columnas ********************************
df.rename(columns={'serie':'ID_feeder'},inplace=True)
df.rename(columns={'feeder':'Feeder'},inplace=True)


def search_id(ID_FEEDER:int):
    '''
    search_id(ID_FEEDER:int)
    toma como parametro el id del feeder,mismo que sera proporcionado por la app feeder status
    mediante el escaneo de los feeders.
    retorna: un dataframe con todos los datos del feeder ( ID_feeder, Feeder )
    '''
    #buscar feeder por id
    if ID_FEEDER in df['ID_feeder'].values:
        resultado = df.loc[df['ID_feeder'] == ID_FEEDER].to_string(index = False)
        return resultado


#************************** Analisis de datos (plan feeders SEM )********************************
#cargar archivo excel
# Abre el archivo CSV en modo lectura
with open('PysimpleGUI\Proyectos\mantto_feeder\data\plan feeders SEM.csv', 'r') as archivo_csv:
    # Crea un lector CSV
    lector_csv = csv.reader(archivo_csv)
    # Obtiene la primera fila del archivo CSV
    primera_fila = next(lector_csv)
    
    # Obtiene los valores del rango A1:H1
    valores_rango = primera_fila[0:1502]  # Índices de columna del rango (0 a 7)
    '''
    # Imprime los valores del rango
    for valor in valores_rango:
        print(valor)
    

    #crear dataframe con los valores obtenidos del csv    
    df = pd.DataFrame(valores_rango)
    print(df)
    '''
    print(df.index)
    
    
#if __name__ == '__main__':
 #   search_id(int(values['-ID_feeder-']))