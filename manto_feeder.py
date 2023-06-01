import PySimpleGUI as sg
import time
from threading import *
import threading
from my_tools import crear_plantilla
from datetime import datetime

#Futuramente en desarrollo cambiar inputs de texto por etiquetas,de momento coloque inputs para ver mejor organizados los elementos
#falta manejar errores (try and except)

def app():
    '''
    Funcion principal de la aplicacion mantto_feeder,esta aplicacion trabaja 
    en conjunto con la app feder_status.py
    
    --Parámetros:
            -ID_feeder: ID del feeder
            -Nombre_Tecnico: Nombre del tecnico
            -Feeder_Status: Estado del feeder
            -Feeder = Descripcion del feeder
            -Tipo_Feeder: [CP,QP,BFC,HOVER]
    '''
    #***************************************************\\ CONFIGURACION //***************************************************
    sg.theme('reddit') #tema de la aplicacion    
    
    #***************************************************\\ LAYOUT //***************************************************
    layout = [
        [sg.Image(r'PysimpleGUI\Proyectos\mantto_feeder\img\LOGO_NAVICO_1_90-black.png',expand_x=False,expand_y=False,enable_events=True,key='-LOGO-'),sg.Push()],
        [sg.Text('COLOR DE LA SEMANA',font=('Helvetica',15,'bold')),sg.Push(),sg.Text('DATA\t\t',font=('Helvetica',15,'bold')),sg.Push()],
        [sg.Input(default_text='ROSA',font=('Helvetica',15),key='-COLORF-', size=(25,200)),sg.Push(),sg.Input(font=('Helvetica',15),key='-DATA-', size=(20, 50)),sg.Button('get data', size=(6, 1), font=('Helvetica',10,"bold"), key='-TEST-'),sg.Push()],
        
        [sg.Text('ID_Feeder',font=('Helvetica',15,'bold')),sg.Push(),sg.Text('\tCOLOR:',font=('Helvetica',15,'bold')),sg.Push(),sg.Text('TECNICO  \t\t\t',font=('Helvetica',15,'bold')),sg.Push()],
        [sg.Input(font=('Helvetica',15),key='-ID_FEEDER-', size=(20, 50)),sg.Push(),sg.Input(font=('Helvetica',15),key='-COLOR-', size=(10, 20)),sg.Push(),sg.Input(default_text='',font=('Helvetica',15),key='-TECH-', size=(38, 80))],
        
        [sg.Text('FEEDER \t\t',font=('Helvetica',15,'bold')),sg.Push(),sg.Text('CODIGO',font=('Helvetica',15,'bold')),sg.Push(),sg.Text('CALIBRACION',font=('Helvetica',15,'bold')),sg.Push(),sg.Push(),sg.Push()],
        [sg.Input(font=('Helvetica',15),key='-DATA-', size=(21, 50)),sg.Push(),sg.Input(font=('Helvetica',15),key='-DATA-', size=(10, 50)),sg.Push(),sg.Push(),sg.Canvas(background_color='gray',size=(150,50),key='-CANVA-'),sg.Push(),sg.Push(),sg.Push(),sg.Push(),sg.Push(),sg.Push()],
        
        [sg.Text("Status",font=('Helvetica',15,'bold'))],
        [sg.Canvas(background_color='gray',size=(900,100),key='-CANVA-')],
        
        [sg.HSeparator()],
        [sg.Text("CP",font=('Helvetica',15)),sg.Combo(values=["NG","OK"],font=('Helvetica',15),size=(5,1),key='-CP-',enable_events=True,readonly=True),sg.Text("\tBFC",font=('Helvetica',15)),sg.Combo(values=["NG","OK"],font=('Helvetica',15),size=(5,1),key='-BFC-',enable_events=True,readonly=True),sg.Push(),sg.Text("Observaciones:\t\t",font=('Helvetica',15,'bold')),sg.Push()],
        [sg.Text("QP",font=('Helvetica',15)),sg.Combo(values=["NG","OK"],font=('Helvetica',15),size=(5,1),key='-QP-',enable_events=True,readonly=True),sg.Text("\tHOVER",font=('Helvetica',15)),sg.Combo(values=["NG","OK"],font=('Helvetica',15),size=(5,1),key='-HOVER-',enable_events=True,readonly=True),sg.Push(),sg.Multiline("" ,size=(50 ,5) ,no_scrollbar=True ,enable_events=True,key='-OBS-'),sg.Push()],
        [sg.Text()]
        ]
    
    window = sg.Window('Manto Feeder Main', layout,element_justification='center')
    while True:
        event, values = window.read()
        #print(event, values)
        if event == sg.WIN_CLOSED:
            break    
        
        #*************\\ Funciones //*************
        def get_data():
            '''
             get data():
                --argumentos:
                    -Nombre_Tecnico: Nombre del tecnico
                    -ID_Feeder: ID del feeder
                    -Tipo_Feeder: [CP,QP,BFC,HOVER]
                --funcionamiento:
                    -Toma los datos de los argumentos anteriormente mecionados
                    y se los pasa como parametros a la funcion create_template() traida
                    del script crear_plantilla.py
            '''
            if values['-CP-'] == "OK":
                Tipo_Feeder = "CP"    
            if values['-QP-'] == "OK":
                Tipo_Feeder = "QP"
            if values['-BFC-'] == "OK":
                Tipo_Feeder = "BFC"
            if values['-HOVER-'] == "OK":
                Tipo_Feeder = "HOVER"
            id_feeder = values['-DATA-'] #toma el valor del input DATA
            window['-ID_FEEDER-'].update(id_feeder) #actualiza el input ID_FEEDER
            copy_id = values['-ID_FEEDER-'] #toma el valor del input ID_FEEDER
            color_f = values['-COLORF-'] #toma el valor del texto
            window['-COLOR-'].update(color_f) #actualiza el input COLOR a el color de semana establecido
            tecnico = values['-TECH-'] #toma el valor del input TECNICO        
            fecha = datetime.now().strftime('%d/%m/%Y')
            observaciones = values['-OBS-']
            return tecnico,id_feeder,Tipo_Feeder,fecha,color_f,observaciones
            #def create_template(Nombre_Tecnico, ID_Feeder, Tipo_Feeder, Fecha_Mantenimiento, Color_Semana):
        
        #****************\\ Simulacion //****************
        
        #*************\\ Eventos //*************
        
        #Obtener datos de GUI
        if event == '-TEST-':
            print(get_data())
            
            #crear plantilla
            #1ra opcion
            #data = list(get_data())
            #crear_plantilla.create_template(data[0],data[1],data[2],data[3],data[4])
            
            #2da opcion
            crear_plantilla.create_template(get_data()[0],get_data()[1],get_data()[2],get_data()[3],get_data()[4],get_data()[5])
        
        
        
    window.close()
    
if __name__ == '__main__':
    app()