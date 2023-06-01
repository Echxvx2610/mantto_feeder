import PySimpleGUI as sg
import time
from threading import *
import threading

#ingresar id solo con escanear y ejecutar despues

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
    sg.theme('graygraygray')
    def reset_status():
        '''
        reset status():
        Espera n segundos y actualiza el valor del background_color del canvas
        '''
        time.sleep(1)
        window['-CANVA-'].update(background_color='gray')
        window['-ID_feeder-'].update('')
    
    def check_status():
        '''
        Check status():
            revisa el estadis del feeder y actualiza el valor del background_color del canvas
            **hace una consulta en el registro excel de los feeders
        
        '''
        window['-CANVA-'].update(background_color='lawn green')
    
    
    
    layout = [
        #[sg.Text('Feder Status',font=('Oswald',20))],
        [sg.Image(r'PysimpleGUI\Proyectos\mantto_feeder\img\LOGO_NAVICO_1_90-black.png',expand_x=False,expand_y=False,enable_events=True,key='-LOGO-')],
        [sg.Text('ID_feeder:',font=('Helvetica',15)),sg.Input(key='-ID_feeder-',size=(20,50),enable_events=True)],
        [sg.Text("Datos Feeder: no disponible aun",key='--')],
        [sg.Canvas(background_color='black',size=(300,300),key='-CANVA-')],
        ]
    
    window = sg.Window('Mantto Feeder Status', layout,element_justification='center',return_keyboard_events=True)
    while True:
        event, values = window.read()
        #print(event, values)
        if event == sg.WIN_CLOSED:
            break
        
        
        if event == '\r':
            if len(values['-ID_feeder-']) == 9:
                check_status()
                hilo = threading.Thread(target=reset_status)
                hilo.start()
            else:
                sg.popup('Feeder no encontrado!!')
                    
    window.close()
      
if __name__ == '__main__':
    feeder_status()
    print(feeder_status.__doc__)