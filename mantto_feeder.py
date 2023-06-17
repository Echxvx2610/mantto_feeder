#-*- coding: utf-8 -*-
import PySimpleGUI as sg
from threading import *
import threading
from my_tools import crear_plantilla,search_feeder
from datetime import datetime,time
import subprocess
import shutil
import time
import csv
import asyncio
import os


#***************************************************\\ ISSUES //***************************************************
            #--> Implementar Try/Except para evitar errores de tipo
            #--> Al copiar y rellenar plantilla se pierde imagen navico group (posible solucion,implementar shutil para copiar documento y editar en base a ese)
            #--> color de semana viene dado por csv mantto seq(trabajando en funcion para obtener fecha y color)
                    

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
            
    --Funciones internas:
            -get data():
                --argumentos:
                    -Nombre_Tecnico: Nombre del tecnico
                    -ID_Feeder: ID del feeder
                    -Tipo_Feeder: [CP,QP,BFC,HOVER]
                --funcionamiento:
                    -Toma los datos de los argumentos anteriormente mecionados
                    y se los pasa como parametros a la funcion create_template() traida
                    del script crear_plantilla.py
            - reset():
                --argumentos:
                    -Nombre_Tecnico: Nombre del tecnico
                    -ID_Feeder: ID del feeder
                    -Tipo_Feeder: [CP,QP,BFC,HOVER]
                    -Color_Feeder: Color del feeder
                --funcionamiento:
                    -Limpia los campos despues de tomar la info recabada por get_data()

    '''
    #***************************************************\\ CONFIGURACION //***************************************************
    sg.theme('LightGrey') #tema de la aplicacion    
    menu_layout = [
        ['File', ['Open','View','Exit']],
        ['Help','About'],
    ]
    
    #***************************************************\\ LAYOUT //***************************************************
    
    layout = [
        #menu
        [sg.Menu(menu_layout,key='-MENU-')],
        [sg.Image(r'PysimpleGUI\Proyectos\mantto_feeder\img\LOGO_NAVICO_1_90-black.png',expand_x=False,expand_y=False,enable_events=True,key='-LOGO-'),sg.Push()],
        [sg.Text('COLOR DE LA SEMANA',font=('Helvetica',15,'bold')),sg.Push(),sg.Text('DATA\t\t',font=('Helvetica',15,'bold')),sg.Push()],
        [sg.Input(default_text="N\A",font=('Helvetica',15),key='-COLORF-', size=(25,200),readonly=True,text_color="blue"),sg.Push(),sg.Input(font=('Helvetica',15),key='-ID_FEEDER-', size=(20, 50)),sg.Push()],
        
        [sg.Text('ID_Feeder',font=('Helvetica',15,'bold')),sg.Push(),sg.Text('\tCOLOR:',font=('Helvetica',15,'bold')),sg.Push(),sg.Text('TECNICO \t\t',font=('Helvetica',15,'bold')),sg.Push()],
        [sg.Input(font=('Helvetica',15),key='-INF_FEEDER-', size=(20, 50),readonly=True,text_color="blue"),sg.Push(),sg.Input(default_text="N\A",font=('Helvetica',15),key='-COLORC-', size=(10,20),readonly=True,text_color="blue"),sg.Push(),sg.Combo(values=["Francisco Rodriguez","Yamcha Cota","Efrain Ramirez"],font=('Helvetica',15),size=(30,1),key='-TECH-',enable_events=True,readonly=True)],
        
        [sg.Text('FEEDER \t\t',font=('Helvetica',15,'bold')),sg.Push(),sg.Text('CODIGO',font=('Helvetica',15,'bold')),sg.Push(),sg.Text('CALIBRACION',font=('Helvetica',15,'bold')),sg.Push(),sg.Push(),sg.Push()],
        [sg.Input(font=('Helvetica',15),key='-DATA-', size=(21, 50),readonly=True,text_color="blue"),sg.Push(),sg.Input(font=('Helvetica',15),key='-DATA-', size=(10, 50),readonly=True,text_color="blue"),sg.Push(),sg.Push(),sg.Canvas(background_color='gray',size=(150,50),key='-CANVAC-'),sg.Push(),sg.Push(),sg.Push(),sg.Push(),sg.Push(),sg.Push()],
        
        [sg.Text("Status",font=('Helvetica',15,'bold'))],
        [sg.Canvas(background_color='gray',size=(800,100),key='-CANVAG-')],
        
        [sg.HSeparator()],
        [sg.Text("CP",font=('Helvetica',15)),sg.Combo(values=["N/A","OK"],font=('Helvetica',15),size=(5,1),key='-CP-',enable_events=True,readonly=True),sg.Text("\tBFC",font=('Helvetica',15)),sg.Combo(values=["N/A","OK"],font=('Helvetica',15),size=(5,1),key='-BFC-',enable_events=True,readonly=True),sg.Push(),sg.Text("Observaciones:\t\t",font=('Helvetica',15,'bold')),sg.Push()],
        [sg.Text("QP",font=('Helvetica',15)),sg.Combo(values=["N/A","OK"],font=('Helvetica',15),size=(5,1),key='-QP-',enable_events=True,readonly=True),sg.Text("\tHOVER",font=('Helvetica',15)),sg.Combo(values=["N/A","OK"],font=('Helvetica',15),size=(5,1),key='-HOVER-',enable_events=True,readonly=True),sg.Push(),sg.Multiline("" ,size=(50 ,5) ,no_scrollbar=True ,enable_events=True,key='-OBS-'),sg.Push()],
        [sg.Text("Created by:Cristian Echevarria",font=('Helvetica',6,'italic'))],
        ]
    
    window = sg.Window('Manto Feeder Main', layout,element_justification='center',return_keyboard_events=True)
    while True:
        event, values = window.read()
        #print(event, values)
        if event == sg.WIN_CLOSED:
            break    
        
        
        
        #*************\\ Funciones //*************
        async def check_status():
            '''
            check_status():
                Verifica si el feeder esta activo o con mantenimiento realizado
            '''
            #buscar feeder por id
            resultado = search_feeder.search_id(int(values['-ID_FEEDER-']))
            #index_fecha = 
            if resultado is not None:
                window["-CANVAG-"].update(background_color='lawn green')
                window["-CANVAC-"].update(background_color='lawn green')
                #window["-ID_feeder-"].update('')   
            if resultado is None:
                window["-CANVAG-"].update(background_color='red')
                window["-CANVAC-"].update(background_color='red')
                sg.popup('Feeder no encontrado!!')
                
        
        async def index_fecha():
            fecha_actual = datetime.now()
            fecha_formateada = fecha_actual.strftime(f'{fecha_actual.month}/{fecha_actual.day}/{fecha_actual.year}')
            resultado = search_feeder.search_fecha(fecha_formateada)[1]
            if resultado is not None:
                window['-COLORF-'].update(resultado)
                window['-COLORC-'].update(resultado)
                
   

        
        def reset():
            '''
            reset():
                Establece el color de los canvas a gris asi como el de los inputs en blanco
            '''
            time.sleep(1 )
            window['-ID_FEEDER-'].update('')
            window['-COLORC-'].update('')
            window['-TECH-'].update('')
            window['-OBS-'].update('')
            window['-CANVAC-'].update(background_color='gray')
            window['-CANVAG-'].update(background_color='gray')
            window['-DATA-'].update('')
            
        def get_data():
            '''
            get_data():
                Recaba informacion del input DATA,TECNICO,TIPO_FEEDER,OBSERVACIONES
            '''
            if values['-CP-'] == "OK":
                Tipo_Feeder = "CP"    
            if values['-QP-'] == "OK":
                Tipo_Feeder = "QP"
            if values['-BFC-'] == "OK":
                Tipo_Feeder = "BFC"
            if values['-HOVER-'] == "OK":
                Tipo_Feeder = "HO0VER"
            id_feeder = values['-ID_FEEDER-'] #toma el valor del input DATA
            window['-INF_FEEDER-'].update(id_feeder) #actualiza el input ID_FEEDER
            copy_id = values['-ID_FEEDER-'] #toma el valor del input ID_FEEDER
            color_f = values['-COLORF-'] #toma el valor del texto
            window['-COLORC-'].update(color_f) #actualiza el input COLOR a el color de semana establecido
            tecnico = values['-TECH-'] #toma el valor del input TECNICO        
            fecha = datetime.now().strftime('%d/%m/%Y')
            observaciones = values['-OBS-']
            return tecnico,id_feeder,Tipo_Feeder,fecha,color_f,observaciones

        #*************\\ Eventos //*************
        #Manejo de errores para evitar bloqueo de app
        '''
        #Obtener datos de GUI   
        if event == '\r':
            print(get_data()) #revisar que valores tomo la funcion get_data
            asyncio.run(check_status())
            get_data()
            #Crear plantilla
            #validamos que no falte ningun dato
            primer_dato,segundo_dato,tercer_dato,cuarto_dato,quinto_dato,sexto_dato = get_data()[0],get_data()[1],get_data()[2],get_data()[3],get_data()[4],get_data()[5]    
            if primer_dato == '' or segundo_dato == '' or tercer_dato == '' or cuarto_dato == '' or quinto_dato == '' or sexto_dato == '':
                sg.popup('Faltan datos por llenar')
            else:
                #Si todo lo anterior esta orden es decir se ha llenado toda la info se genera un reporte
                crear_plantilla.create_template(get_data()[0],get_data()[1],get_data()[2],get_data()[3],get_data()[4],get_data()[5])
                generador = threading.Thread(target=reset,daemon=True)
                generador.start()
                sg.popup('Reporte generado con exito!')
                reset()
        '''
        
        try:
            #Obtener datos de GUI   
            if event == '\r':
                print(get_data()) #revisar que valores tomo la funcion get_data
                asyncio.run(check_status())
                asyncio.run(index_fecha())
                get_data()
                #Crear plantilla
                #validamos que no falte ningun dato
                primer_dato,segundo_dato,tercer_dato,cuarto_dato,quinto_dato,sexto_dato = get_data()[0],get_data()[1],get_data()[2],get_data()[3],get_data()[4],get_data()[5]    
                if primer_dato == '' or segundo_dato == '' or tercer_dato == '' or cuarto_dato == '' or quinto_dato == '' or sexto_dato == '':
                    sg.popup('Faltan datos por llenar')
                else:
                    #Si todo lo anterior esta orden es decir se ha llenado toda la info se genera un reporte
                    crear_plantilla.create_template(get_data()[0],get_data()[1],get_data()[2],get_data()[3],get_data()[4],get_data()[5])
                    generador = threading.Thread(target=reset,daemon=True)
                    generador.start()
                    sg.popup('Reporte generado con exito!')
                    reset()
        except UnboundLocalError:
            title = "Excepcion!"
            message = """-! Ocurrio un error.\nAsegurese de haber introduccido el ID del feeder o haber seleccionado un tipo de feeder"""
            sg.popup(message, title=title)
        except ValueError:
            title = "Excepcion!"
            message = """-! Ocurrio un error al leer el ID del feeder.\nAsegurese de haber introduccido el ID del feeder o haber seleccionado un tipo de feeder\nEl ID debe ser numérico!!"""
            sg.popup(message, title=title)
        except:
            title = "Excepcion!"
            message = """-!Ocurrio un error al procesar los datos.\nAntes de comenzar escanee el ID del feeder.\nSi el problema consiste contacta al Equipo de MFG."""
            sg.popup(message, title=title)

        #Eventos de menu
        if values['-MENU-'] == "Open":
            sg.popup_get_file("Seleccione un archivo",file_types=(("Excel files", "*.xlsx"), ("All files", "*.*")))
        elif values['-MENU-'] == "About":
            title = "Contacto"
            message = """-Created by: Cristian Echevarria,Version: 1.0\n-Email:cristianecheverriamendoza@gmail.com\n-Tel: 6462567733-Ensenada,B.C\n"""
            sg.popup(message, title=title)
        elif values['-MENU-'] == "View":
            #abre app feeder_status
            #second_app = threading.Thread(target=feeder_status,daemon=True)
            #second_app.start()
            
            # Ruta al archivo de Excel que deseas abrir
            archivo_excel = r"C:\Users\CECHEVARRIAMENDOZA\OneDrive - Brunswick Corporation\Documents\Proyectos_Python\PysimpleGUI\Proyectos\mantto_feeder\data\plan feeders SEM.csv"
            # Comando para abrir el archivo con Excel
            comando_abrir_excel = f'start excel "{archivo_excel}"'

            # Ejecutar el comando para abrir el archivo con Excel
            os.system(comando_abrir_excel)
                                
    window.close()  

#print(app.__doc__) 

if __name__ == '__main__':
    app()