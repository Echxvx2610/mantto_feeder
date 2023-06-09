import PySimpleGUI as sg
import time
from threading import *
import threading
import subprocess
import asyncio

#Reto: ingresar id solo con escanear y ejecutar despues

def feeder_status():
    '''
    Funcion principal de la aplicacion feder_status.py
    feder_status.py valida el estado del feeder en cuestion.
    
    --Parámetros:
            -ID_feeder: ID del feeder
    
    --Funcion:
            -Revisa el estado del feeder(mantenimiento) ingresando el ID
            -Despliega con colores la condicion del feeder
        
    
    '''
    #definicion de tema
    sg.theme('graygraygray')
    
    #*********************************** Funciones asyncronas (pruebas) ***********************************
    async def check_status():
        '''
        Check status():
            revisa el estadis del feeder y actualiza el valor del background_color del canvas
            **hace una consulta en el registro excel de los feeders
        
        '''
        window['-CANVA-'].update(background_color='lawn green')
        await asyncio.sleep(0.5)
        window['-ID_feeder-'].update('')
        
    
    
    async def reset_status():
        '''
        reset status():
        funcion asyncrona para resetear el estado del feeder
        Espera n segundos y actualiza el valor del background_color del canvas siempre y cuando check_status() haya terminado
        '''
        await check_status()
        window['-CANVA-'].update(background_color='red')
        await asyncio.sleep(0.5)
        window['-ID_feeder-'].update('')
    
    
    
    #********************************************\\ LAYOUT //*****************************************************
    
    
    layout = [
        #[sg.Text('Feder Status',font=('Oswald',20))],
        [sg.Image(r'img\LOGO_NAVICO_1_90-black.png',expand_x=False,expand_y=False,enable_events=True,key='-LOGO-')],
        [sg.Text('ID_feeder:',font=('Helvetica',15)),sg.Input(key='-ID_feeder-',size=(20,50),enable_events=True)],
        [sg.Text("Datos Feeder: no disponible aun",key='--')],
        [sg.Canvas(background_color='black',size=(300,300),key='-CANVA-')],
        ]
    
    window = sg.Window('Mantto Feeder Status', layout,element_justification='center',return_keyboard_events=True)
    while True:
        event, values = window.read(timeout=10)
        #print(event, values)
        if event == sg.WIN_CLOSED:
            break
        
        #***********************************\\ Pruebas con scanner //***********************************
        
        #EVENTO PARA BUSCAR EL ESTADO DEL FEEDER(INCORPORAR LECTURA DE EXCEL EN LUGAR DE LISTA)
        lista_feeders = ["104554539","104554540","104554541","104554542","104554543","105372565"]
        try:
            if len(values['-ID_feeder-']) == 9:
                if values['-ID_feeder-'] in lista_feeders:
                    asyncio.run(check_status())
            if len(values['-ID_feeder-']) == 9:
                if values['-ID_feeder-'] not in lista_feeders:
                    asyncio.run(reset_status())
        except:
            print("Error")
        '''
        if event == '\r':
            if len(values['-ID_feeder-']) == 9:
                check_status()
                #script para abrir aplicaciones .exe
                # import subprocess
                # ruta_programa = r'C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE'
                # # Ejecutar el programa
                # subprocess.run(ruta_programa)
                hilo = threading.Thread(target=reset_status)
                hilo.start()
            else:
                sg.popup('Feeder no encontrado!!')
        '''
        #****************************************************************************************`         
    window.close()
      
if __name__ == '__main__':
    feeder_status()
    print(feeder_status.__doc__)