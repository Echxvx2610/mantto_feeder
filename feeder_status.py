import PySimpleGUI as sg
import time
from threading import *
import threading

def feeder_status():
    '''
    Funcion principal de la aplicacion feder_status.py
    aplicacion feder_status.py valida el estado del feeder en cuestion.
    
    --Parámetros:
            -ID_feeder: ID del feeder
    
    
    '''
    sg.theme('graygraygray')
    def reset_status():
        '''
        funcion reset status():
        espera n segundos y actualiza el valor del background_color del canvas
        '''
        time.sleep(3)
        window['-CANVA-'].update(background_color='gray')
    
    layout = [
        #[sg.Text('Feder Status',font=('Oswald',20))],
        [sg.Text('ID_feeder:',font=('Helvetica',15)),sg.Input(key='ID_feeder',size=(20,50))],
        [sg.Canvas(background_color='black',size=(300,300),key='-CANVA-')],
        [sg.Button('TEST', size=(15, 2), font=('Helvetica', 14,"bold"), key='-TEST-',border_width=10)],
        ]
    
    window = sg.Window('Mantto Feeder Status', layout,element_justification='center')
    while True:
        event, values = window.read()
        #print(event, values)
        if event == sg.WIN_CLOSED:
            break
        
        if event == '-TEST-':
            if values['ID_feeder'] == '23760055':
                print(conexion)
                window['-CANVA-'].update(background_color='lawn green')
                hilo = threading.Thread(target=reset_status)
                hilo.start() 
            else:
                window['-CANVA-'].update(background_color='red')
                hilo = threading.Thread(target=reset_status)
                hilo.start()    
            
        
        
    window.close()
      
if __name__ == '__main__':
    feeder_status()
    print(app.__doc__)