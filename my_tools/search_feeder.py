#-*- coding: utf-8 -*-
import csv
import pandas as pd
import openpyxl
from openpyxl import workbook,load_workbook
from openpyxl.utils import get_column_letter
from datetime import datetime,time
#*********************** Configuracion de dataframe(muestra todo el dataframe)********************
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)

#***************************** Creacion de un dataframe ********************************
data = pd.read_csv(r'C:\Users\CECHEVARRIAMENDOZA\OneDrive - Brunswick Corporation\Documents\Proyectos_Python\PysimpleGUI\Proyectos\mantto_feeder\data\plan feeders SEM.csv',encoding='ISO-8859-1',usecols=['serie','feeder'])
df = pd.DataFrame(data)
#**************************** Renombrar columnas ********************************
df.rename(columns={'serie':'ID_feeder'},inplace=True)
df.rename(columns={'feeder':'Feeder'},inplace=True)

#apertura del archivo csv (plan feeders SEM)
with open(r'C:\Users\CECHEVARRIAMENDOZA\OneDrive - Brunswick Corporation\Documents\Proyectos_Python\PysimpleGUI\Proyectos\mantto_feeder\data\plan feeders SEM.csv', 'r') as plan_semanal:
    # Crea un lector CSV
    lector_csv = csv.reader(plan_semanal)
    # Obtiene la primera fila del archivo CSV
    primera_fila = next(lector_csv)

    # Obtiene los valores del rango A1:H1
    valores_rango = primera_fila[0:1502]  # Índices de las columnas que tienen por nombre las fechas del año
    '''
    # Imprime los valores del rango
    for valor in valores_rango:
        print(valor)
    '''
    #Crear dataframe con los valores obtenidos del csv(columnas fechas)    
    data_fecha = pd.DataFrame(valores_rango)

with open(r"C:\Users\CECHEVARRIAMENDOZA\OneDrive - Brunswick Corporation\Documents\Proyectos_Python\PysimpleGUI\Proyectos\mantto_feeder\data\mantto seq.csv") as mantto_seq:
    #Crear un lector
    lectura_mantto = csv.reader(mantto_seq)
    data_mantto = pd.read_csv(r"C:\Users\CECHEVARRIAMENDOZA\OneDrive - Brunswick Corporation\Documents\Proyectos_Python\PysimpleGUI\Proyectos\mantto_feeder\data\mantto seq.csv",encoding = "ISO-8859-1",usecols=['DIA','COLOR'])
    df_mantto = pd.DataFrame(data_mantto)
    #print(df_mantto)

def search_id(ID_FEEDER:int):
    '''
    search_id(ID_FEEDER:int)
        toma como parametro el id del feeder,mismo que sera proporcionado por la app feeder status
        mediante el escaneo de los feeders.
        retorna: un dataframe con todos los datos del feeder ( ID_feeder, Feeder )  
        
        extra:
            -Index ID_feeder: index de ID_feeder(posicion del dato en csv)
            -Index fecha: index de fecha (posicion del dato en csv)
    '''
    #buscar feeder por id
    if ID_FEEDER in df['ID_feeder'].values:
        #valores de index feeder y fecha "erroneos" solo para guiarse en CSV
        resultado = df.loc[df['ID_feeder'] == ID_FEEDER].to_string(index = False)
        #Obtener index de feeder
        valor_feeder = ID_FEEDER
        indice_feeder = int(df['ID_feeder'].index[df['ID_feeder']==valor_feeder][0]) + 2
        print("Indice feeder: ",indice_feeder)
        #Obtener index de fecha
        fecha_actual = datetime.now()
        fecha_formateada = fecha_actual.strftime(f'{fecha_actual.month}/{fecha_actual.day}/{fecha_actual.year}')
        valor_fecha = fecha_formateada
        indice_fecha = int(data_fecha[0].index[data_fecha[0]==valor_fecha][0]) + 1
        print('Indice de fecha buscada: ',indice_fecha)
        id_feeder = resultado.split()
        descripcion = id_feeder[3]
        return resultado   

#************************** Analisis de datos (plan feeders SEM )********************************
def cell_value(ID_FEEDER:int):
    '''
    cell_value(ID_FEEDER:int)
        retorna una tupla con los valores de interseccion entre el id de un feeder respecto a la columna fecha,color y codigo
    '''
    #cargar archivo excel
    # Abre el archivo CSV en modo lectura
    with open(r'C:\Users\CECHEVARRIAMENDOZA\OneDrive - Brunswick Corporation\Documents\Proyectos_Python\PysimpleGUI\Proyectos\mantto_feeder\data\plan feeders SEM.csv', 'r') as plan_semanal:
        # Crea un lector CSV
        lector_csv = csv.reader(plan_semanal)
        # Obtiene la primera fila del archivo CSV
        primera_fila = next(lector_csv)
        # Obtiene los valores del rango A1:H1
        valores_rango = primera_fila[0:1502]  # Índices de las columnas que tienen por nombre las fechas del año
    
        #Crear dataframe con los valores obtenidos del csv(columnas)    
        data_fecha = pd.DataFrame(valores_rango)
        try:
            #Valores de index feeder y fecha "Exactos" para analisis de CSV
            #Obtener index de feeder
            valor_feeder = ID_FEEDER
            indice_feeder = int(df['ID_feeder'].index[df['ID_feeder']==valor_feeder][0])
            print("Indice feeder: ",indice_feeder + 2) # + 2 debido al index
            #Obtener index de fecha
            fecha_actual = datetime.now()
            fecha_formateada = fecha_actual.strftime(f'{fecha_actual.month}/{fecha_actual.day}/{fecha_actual.year}')
            valor_fecha = fecha_formateada
            indice_fecha = int(data_fecha[0].index[data_fecha[0]==valor_fecha][0])
            print('Indice de fecha buscada: ',indice_fecha + 1) # + 1 debido al index

            #comprobar si hay un OK en una interseccion data por el index de un feeder y el index de una fecha(funcionando)
            csv_data  = list(lector_csv)
            fila = indice_feeder #al index deseado restarle 2 por conflicto con index
            columna_fecha = indice_fecha #igual a 3 por el 0 del index
            columna_color = 3
            columna_codigo = 2
            #Obtener valor de interseccion con columna fecha
            if fila < len(csv_data) and columna_fecha < len(csv_data[0]):
                #obtener valor de interseccion
                interseccion_fecha = csv_data[fila][columna_fecha]
            else:
                print("No se encontro valor interseccion")

            #Obtener valor de interseccion con columna color
            if fila < len(csv_data) and columna_color < len(csv_data[0]):
                #obtener valor de interseccion
                interseccion_color = csv_data[fila][columna_color]
            else:
                print("No se encontro valor interseccion")

            #Obtener valor de interseccion con columna codigo
            if fila < len(csv_data) and columna_codigo < len(csv_data[0]):
                #obtener valor de interseccion
                interseccion_codigo = csv_data[fila][columna_codigo]
            else:
                print("No se encontro valor interseccion")

            return interseccion_fecha, interseccion_color, interseccion_codigo
        except:
            return 0, 0, 0
def search_fecha(FECHA:str):
    '''
    search_id(ID_FEEDER:int)
        toma como parametro el id del feeder,mismo que sera proporcionado por la app feeder status
        mediante el escaneo de los feeders.
        retorna: un dataframe con todos los datos del feeder ( ID_feeder, Feeder )  
        
        extra:
            -Index ID_feeder: index de ID_feeder(posicion del dato en csv)
            -Index fecha: index de fecha (posicion del dato en csv)
    '''
    #fecha en columna
    index_fecha = df_mantto.loc[df_mantto['DIA'] == FECHA].to_string(index = False)
    index_fecha = index_fecha.split()
    dia = index_fecha[2]
    color = index_fecha[3]
    return dia, color
    
#Quitar comentarios para testear
#print(search_id(104575035)) #probar funcionamiento de funcion
#print("\n")
#print(cell_value(104575035)[0]) #probar funcionamiento de funcion
fecha_actual = datetime.now()
fecha_formateada = fecha_actual.strftime(f'{fecha_actual.month}/{fecha_actual.day}/{fecha_actual.year}')   
#print(search_fecha(fecha_formateada)[1]) #probando funcion para buscar fecha