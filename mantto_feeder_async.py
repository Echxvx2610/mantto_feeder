#-*- coding: utf-8 -*-
import PySimpleGUI as sg
from threading import *
import threading
from tools import crear_plantilla,search_feeder,progress,loggin,validar
from datetime import datetime,time
import subprocess
import shutil
import time
import csv
import asyncio
import os


#***************************************************\\ ISSUES //***************************************************
#--> Actulizar App en estacion feeder repair
#***************************************************************************************************************
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
                    -Fecha = Fecha de mantenimiento
                --funcionamiento:
                    -Toma los datos de los argumentos anteriormente mecionados
                    y se los pasa como parametros a la funcion create_template() traida
                    del modulo crear_plantilla.py
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
    #layout del menu
    menu_layout = [
        ['File', ['Open','View','Exit']],
        ['Help','About']
    ]
    
    #***************************************************\\ LAYOUT //***************************************************
    
    layout = [
        #menu
        [sg.Menu(menu_layout,key='-MENU-')],
        [sg.Image(r'mantto_feeder\img\LOGO_NAVICO_1_90-black.png',expand_x=False,expand_y=False,enable_events=True,key='-LOGO-'),sg.Push()],
        [sg.Text('COLOR DE LA SEMANA',font=('Helvetica',15,'bold')),sg.Push(),sg.Text('DATA\t\t',font=('Helvetica',15,'bold')),sg.Push()],
        [sg.Input(default_text="N\A",font=('Helvetica',15),key='-COLORF-', size=(25,200),readonly=True,text_color="blue"),sg.Push(),sg.Input(font=('Helvetica',15),key='-ID_FEEDER-',readonly=False,text_color='white',enable_events=True,size=(20, 50)),sg.Push()],
        
        [sg.Text('ID_Feeder',font=('Helvetica',15,'bold')),sg.Push(),sg.Text('\tCOLOR:',font=('Helvetica',15,'bold')),sg.Push(),sg.Text('TECNICO \t\t',font=('Helvetica',15,'bold')),sg.Push()],
        [sg.Input(font=('Helvetica',15),key='-INF_FEEDER-', size=(20, 50),readonly=True,text_color="blue"),sg.Push(),sg.Input(default_text="N\A",font=('Helvetica',15),key='-color-', size=(10,20),readonly=True,text_color="blue"),sg.Push(),sg.Input(default_text="N\A",font=('Helvetica',15),key='-TECH-',readonly=True,text_color='blue',enable_events=True,size=(35, 50))],
        
        [sg.Text('FEEDER \t\t',font=('Helvetica',15,'bold')),sg.Push(),sg.Text('CODIGO',font=('Helvetica',15,'bold')),sg.Push(),sg.Text('CALIBRACION',font=('Helvetica',15,'bold')),sg.Push(),sg.Push(),sg.Push()],
        [sg.Input(font=('Helvetica',15),key='-DESCRIP-', size=(21, 50),readonly=True,text_color="blue",enable_events=True),sg.Push(),sg.Input(font=('Helvetica',15),key='-DATA-', size=(10, 50),readonly=True,text_color="blue"),sg.Push(),sg.Push(),sg.Canvas(background_color='gray',size=(150,50),key='-CANVAC-'),sg.Button('Calibrar',font=('Helvetica',15),size=(7,1),key='-CALIB-',enable_events=True),sg.Button('Reset',font=('Helvetica',15),size=(5,1),key='-RESET-',enable_events=True),sg.Push(),sg.Push(),sg.Push()],
        
        [sg.Text("Status",font=('Helvetica',15,'bold'))],
        [sg.Canvas(background_color='gray',size=(800,100),key='-CANVAG-')],
        
        [sg.HSeparator()],
        [sg.Text("CP",font=('Helvetica',15)),sg.Combo(values=["N/A","OK"],font=('Helvetica',15),size=(5,1),key='-CP-',enable_events=True,readonly=True),sg.Text("\tBFC",font=('Helvetica',15)),sg.Combo(values=["N/A","OK"],font=('Helvetica',15),size=(5,1),key='-BFC-',enable_events=True,readonly=True),sg.Push(),sg.Text("Observaciones:\t\t",font=('Helvetica',15,'bold')),sg.Push()],
        [sg.Text("QP",font=('Helvetica',15)),sg.Combo(values=["N/A","OK"],font=('Helvetica',15),size=(5,1),key='-QP-',enable_events=True,readonly=True),sg.Text("\tHOVER",font=('Helvetica',15)),sg.Combo(values=["N/A","OK"],font=('Helvetica',15),size=(5,1),key='-HOVER-',enable_events=True,readonly=True),sg.Push(),sg.Multiline("" ,size=(50 ,5) ,no_scrollbar=True ,enable_events=True,key='-OBS-'),sg.Push()],
        [sg.Text("Created by:Cristian Echevarria",font=('Helvetica',8,'italic'))],
        ]
    
    window = sg.Window('Manto Feeder Main', layout,element_justification='center',return_keyboard_events=True,icon=r"mantto_feeder\img\mantto.ico")
    while True:
        event, values = window.read()
        #print(event, values)
        if event == sg.WIN_CLOSED:
            break    
        
        #loggin.login()
        #if inicio_exitoso == True:
        #    pass
        #else:
        #    break   #quitar comentario para implementar sistema de loggin
        
        
        #**********************************************\\ Funciones //****************************************************
        async def check_status():
            '''
            check_status():
                Verifica si el feeder esta activo o con mantenimiento realizado
            '''
            try:
                #buscar feeder por id(en archivo Plan Semanal.xlsx)
                resultado = search_feeder.search_id(int(values['-ID_FEEDER-']))
                #valor de interseccion(ID_FEEDER * fecha)
                valor_de_celda = search_feeder.cell_value(int(values['-ID_FEEDER-']))[0]
                #consultar valor de codigo en xlsx
                codigo = search_feeder.cell_value(int(values['-ID_FEEDER-']))[2]
                #consultar color de feeder
                color_feeder = search_feeder.cell_value(int(values['-ID_FEEDER-']))[1]
                #Fecha formateada(MM/DD/YYYY)
                fecha_actual = datetime.now()
                fecha_formateada = fecha_actual.strftime(f'{fecha_actual.month}/{fecha_actual.day}/{fecha_actual.year}')
                #buscamos el color de la semana dada la fecha en el archivo mantto seq.csv
                data_fecha = search_feeder.search_fecha(fecha_formateada)[1]
                #consultar descripcion de feeder
                # El retorno de search_id se convierte en lista y tomamos del index 3 en adelante
                # con el bucle for interamos sobre esa lista segun el tamaño y creamos una descripcion ajustable
                descripcion = ""
                for i in search_feeder.search_id(int(values['-ID_FEEDER-'])).split()[3:]:
                    descripcion += i + " "
                    
                if valor_de_celda == "OK":
                    window['-INF_FEEDER-'].update(values['-ID_FEEDER-'])
                    window['-ID_FEEDER-'].update("")
                    window['-ID_FEEDER-'].update(disabled=True)
                    window["-CANVAG-"].update(background_color='lawn green')
                    window["-CANVAC-"].update(background_color='lawn green')
                    window['-color-'].update(color_feeder)
                    window['-COLORF-'].update(data_fecha)
                    window['-DESCRIP-'].update(descripcion)
                    window['-DATA-'].update(codigo)
                elif valor_de_celda == "P":
                    window['-INF_FEEDER-'].update(values['-ID_FEEDER-'])
                    window['-ID_FEEDER-'].update("")
                    window['-ID_FEEDER-'].update(disabled=True)
                    window["-CANVAG-"].update(background_color='Red')
                    window["-CANVAC-"].update(background_color='Red')
                    window['-color-'].update(color_feeder)
                    window['-COLORF-'].update(data_fecha)
                    window['-DESCRIP-'].update(descripcion)
                    window['-DATA-'].update(codigo)
                else:
                    window['-INF_FEEDER-'].update(values['-ID_FEEDER-'])
                    window['-ID_FEEDER-'].update("")
                    window['-ID_FEEDER-'].update(disabled=True,text_color='blue')
                    window['-color-'].update(color_feeder)
                    window['-COLORF-'].update(data_fecha)
                    window["-CANVAG-"].update(background_color='Red')
                    window["-CANVAC-"].update(background_color='Red')
                    window['-DESCRIP-'].update(descripcion)
                    window['-DATA-'].update(codigo)
                    
            except ValueError:
                title = "Excepcion!"
                message = """-! El ID del feeder debe ser un valor numerico\n Asegurese de haber introduccido el ID del feeder correctamente!"""
                asyncio.run(reset())
                sg.popup(message, title=title)
            # except Exception as e:
            #     # Guardar errores o excepciones en un archivo de texto
            #     with open('mantto_feeder\data\errores.txt', 'a') as file:
            #         timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            #         error_message = f"{timestamp} - Error en la función check_status: {str(e)}\n"
            #         file.write(error_message)

            #         # Resto del código para manejar la excepción
            #         title = "Excepcion!"
            #         message = f"""-! Se ha producido una excepción. Detalles:\n {str(e)}"""
            #         asyncio.run(reset())
            #         sg.popup(message, title=title)
                
            
            
        
        async def reset():
            '''
            reset():
                Establece el color de los canvas a amarillo asi como el de los inputs en blanco
            '''
            window['-ID_FEEDER-'].update('')
            window['-color-'].update('N\A')
            window['-TECH-'].update('N\A')
            window['-OBS-'].update('')
            window['-CANVAC-'].update(background_color='gray')
            window['-CANVAG-'].update(background_color='gray')
            window['-DATA-'].update('')
            window['-INF_FEEDER-'].update('')
            window['-ID_FEEDER-'].update(text_color='white',disabled=False)
            #window["-COLORF-"].update('N\A')
            window['-CP-'].update('')
            window['-QP-'].update('')
            window['-BFC-'].update('')
            window['-HOVER-'].update('')
            window['-CP-'].update(disabled=False)
            window['-QP-'].update(disabled=False)
            window['-BFC-'].update(disabled=False)
            window['-HOVER-'].update(disabled=False)
            window['-DESCRIP-'].update('')
            
        def check_tech():
            a = False
            while a == False:
                usuario = sg.PopupGetText("Numero de empleado:",title='Validar numero de empleado')
                resultado = validar.user(usuario)
                window['-TECH-'].update(resultado)
                if resultado is not None:
                    a = True
                    return resultado
                else:
                    sg.popup_error('Usuario no valido')
                    respuesta = sg.popup_yes_no("Volver a intentar?")
                    if respuesta == "Yes":
                        a = False
                    else:
                        a = True
                        
                
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
                Tipo_Feeder = "HOOVER"
            id_feeder = values['-INF_FEEDER-'] #toma el valor del ID_FEEDER
            #window['-INF_FEEDER-'].update(id_feeder) #actualiza el input ID_FEEDER
            #copy_id = values['-ID_FEEDER-'] #toma el valor del input ID_FEEDER
            color_f = values['-color-']
            #tecnico = values['-TECH-'] #toma el valor del input TECNICO        
            #window['-TECH-'].update(validar.user())
            tecnico = values['-TECH-']
            fecha_actual = datetime.now()
            dia = fecha_actual.day
            mes = fecha_actual.strftime('%b')
            año = fecha_actual.year
            fecha = "{}{}{}".format(dia,mes,año)
            observaciones = values['-OBS-']
            return tecnico,id_feeder,Tipo_Feeder,fecha,color_f,observaciones
        
        
        #*************\\ Eventos //*************
        #Manejo de errores para evitar bloqueo de app
        if event == '-RESET-':
            asyncio.run(reset())
        
        if event in ['-CP-', '-QP-', '-BFC-', '-HOVER-']:
            window['-CP-'].update(disabled=True)
            window['-QP-'].update(disabled=True)
            window['-BFC-'].update(disabled=True)
            window['-HOVER-'].update(disabled=True)
        
        try:
            if len(values['-ID_FEEDER-']) == 9:
                asyncio.run(check_status())
        except:
            message = """-! El ID del feeder debe ser un valor numerico\n Asegurese de haber introduccido el ID del feeder correctamente!"""
            title = "Excepcion!"
            window['-ID_FEEDER-'].update('')
            sg.popup(message, title=title)
        try:
            #Obtener datos de GUI   
            if event == '-CALIB-':
                #check_tech()
                datos = get_data()
                #Crear plantilla
                #validamos que no falte ningun dato
                """
                primer_dato,segundo_dato,tercer_dato,cuarto_dato,quinto_dato,sexto_dato = get_data()[0],get_data()[1],get_data()[2],get_data()[3],get_data()[4],get_data()[5]    
                if primer_dato == '' or segundo_dato == '' or tercer_dato == '' or cuarto_dato == '' or quinto_dato == '' or sexto_dato == '':
                sg.popup_error('Faltan datos por llenar!')
                print(get_data()) #revisar que valores tomo la funcion get_data
                """
                if any(dato == '' for dato in get_data()):
                    sg.popup_error('Faltan datos por llenar!')
                    print(get_data()) #revisar que valores tomo la funcion get_data
                else:
                    #Si todo lo anterior esta orden es decir se ha llenado toda la info se genera un reporte
                    crear_plantilla.create_template(check_tech(),get_data()[1],get_data()[2],get_data()[3],get_data()[4],get_data()[5])
                    #rellena rango de celdas en xlsx
                    search_feeder.rellenar_rango_hasta_P(search_feeder.index_ff(int(values['-INF_FEEDER-']))[0],search_feeder.index_ff(int(values['-INF_FEEDER-']))[1])
                    progress.progress_bar()
                    #print(get_data()) #revisar que valores tomo la funcion get_data
                    sg.popup('Reporte generado con exito!')
                    asyncio.run(reset())  
        except UnboundLocalError:
            title = "Excepcion!"
            message = """-! Ocurrio un error.\nAsegurese de haber introduccido el ID del feeder o haber seleccionado un tipo de feeder"""
            sg.popup(message, title=title)
        except ValueError:
            title = "Excepcion!"
            message = """-! Ocurrio un error al leer el ID del feeder.\nAsegurese de haber introduccido el ID del feeder correctamente!"""
            sg.popup(message, title=title)
        except:
            title = "Excepcion!"
            message = """-!Ocurrio un error al procesar los datos.\nAntes de comenzar escanee el ID del feeder.\nSi el problema consiste contacta al Equipo de MFG."""
            sg.popup(message, title=title)
        #Eventos de menu
        if values['-MENU-'] == "Open":
            sg.popup_get_file("Seleccione un archivo",file_types=(("Excel files", "*.xlsx"), ("All files", "*.*")))
        if values['-MENU-'] == "About":
            title = "Contacto"
            message = """-Created by: Cristian Echevarria,Version: 1.0\n-Email:cristianecheverriamendoza@gmail.com"""
            sg.popup(message, title=title)
        elif values['-MENU-'] == "View":
            #abre app feeder_status
            #second_app = threading.Thread(target=feeder_status,daemon=True)
            #second_app.start()
        
        
            # Ruta al archivo de Excel a abrir
            archivo_excel = r"mantto_feeder\data\plan feeders SEM.csv"
            # Comando para abrir el archivo con Excel
            comando_abrir_excel = f'start excel "{archivo_excel}"'
            # Ejecutar el comando para abrir el archivo con Excel
            os.system(comando_abrir_excel)
                                
    window.close()  

#print(app.__doc__) 

if __name__ == '__main__':
    app()
    