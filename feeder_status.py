#-*- coding: utf-8 -*-
import PySimpleGUI as sg
import time
import asyncio
from my_tools import search_feeder

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
            revisa el estado del feeder y actualiza el valor del background_color del canvas
            **hace una consulta en el registro excel de los feeders
        '''
        valores = search_feeder.cell_value(int(values['-ID_feeder-']))
        status = search_feeder.search_id(int(values['-ID_feeder-']))
        valor_intercecion = valores[0]
        if valor_intercecion == "OK":
            window['-CANVA-'].update(background_color='lawn green')
            window['-STATUS-'].update(status)
            window['-ID_feeder-'].update('')
            print(valor_intercecion)
        elif valor_intercecion == "":
            window['-CANVA-'].update(background_color='red')
            window['-ID_feeder-'].update('')
            sg.popup_error('Feeder fuera de registro!!',title=':/')
        else:
            window['-CANVA-'].update(background_color='red')
            window['-ID_feeder-'].update('')
            print(valor_intercecion)
            
        
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
        window['-STATUS-'].update('')
    
    
    
    #********************************************\\ LAYOUT //*****************************************************
    
    layout = [
        #[sg.Text('Feder Status',font=('Oswald',20))],
        [sg.Image(r'mantto_feeder\img\LOGO_NAVICO_1_90-black.png',expand_x=False,expand_y=False,enable_events=True,key='-LOGO-')],
        [sg.Text('ID_feeder:',font=('Avenir Next LT Pro Demi',15)),sg.Input(key='-ID_feeder-',size=(20,50),enable_events=True)],
        [sg.Text("Datos Feeder:",font=('Avenir Next LT Pro Demi',12,'bold'))],
        [sg.Text('',font=('Avenir Next LT Pro Demi',9,'bold'),key='-STATUS-')],
        [sg.Canvas(background_color='gray',size=(300,300),key='-CANVA-',border_width=25)],
        ]
    
    window = sg.Window('Mantto Feeder Status', layout,element_justification='center',return_keyboard_events=True)
    while True:
        event, values = window.read(timeout=10)
        #print(event, values)
        if event == sg.WIN_CLOSED:
            break
        
        #******************************************* Funcion principal de la applicacion ********************************
        try:
            if len(values['-ID_feeder-']) == 9:
                    asyncio.run(check_status())
        except:
            window['-CANVA-'].update(background_color='red')
            window['-STATUS-'].update('')
            title = "Excepción!!"
            message = """-Ocurrio un error al consultar el estado del feeder.\nSi el problema persiste, contacte a MFG"""
            sg.popup(message, title=title)
            window['-ID_feeder-'].update('')

        #****************************************************************************************       
    window.close()
      
if __name__ == '__main__':
     feeder_status()
#    print(feeder_status.__doc__)