import PySimpleGUI as sg
from feeder_status import *

#futuramente en desarrollo cambiar inputs de texto por etiquetas,de momento coloque inputs para ver mejor organizados los elementos


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
    sg.theme('reddit')
    
    layout = [
        [sg.Text('COLOR DE LA SEMANA',font=('Helvetica',15,'bold')),sg.Push(),sg.Text('DATA\t\t',font=('Helvetica',15,'bold')),sg.Button("test"),sg.Push()],
        [sg.Input(default_text='ROSA',font=('Helvetica',15),key='-COLOR-', size=(25,200)),sg.Push(),sg.Input(font=('Helvetica',15),key='-DATA-', size=(20, 50)),sg.Push()],
        [sg.Text('ID_FEEDER',font=('Helvetica',15,'bold')),sg.Push(),sg.Text('\tCOLOR:',font=('Helvetica',15,'bold')),sg.Push(),sg.Text('TECNICO  \t\t\t',font=('Helvetica',15,'bold')),sg.Push()],
        [sg.Input(font=('Helvetica',15),key='-DATA-', size=(20, 50)),sg.Push(),sg.Input(font=('Helvetica',15),key='-DATA-', size=(10, 20)),sg.Push(),sg.Input(default_text='Nombre Tecnico',font=('Helvetica',15),key='-DATA-', size=(38, 80))],
        [sg.Text('FEEDER \t\t',font=('Helvetica',15,'bold')),sg.Push(),sg.Text('CODIGO',font=('Helvetica',15,'bold')),sg.Push(),sg.Text('CALIBRACION',font=('Helvetica',15,'bold')),sg.Push(),sg.Push(),sg.Push()],
        [sg.Input(font=('Helvetica',15),key='-DATA-', size=(21, 50)),sg.Push(),sg.Input(font=('Helvetica',15),key='-DATA-', size=(10, 50)),sg.Push(),sg.Push(),sg.Canvas(background_color='green',size=(150,50),key='-CANVA-'),sg.Push(),sg.Push(),sg.Push(),sg.Push(),sg.Push(),sg.Push()],
        [sg.Text("Status",font=('Helvetica',15,'bold'))],
        [sg.Canvas(background_color='gold',size=(900,100),key='-CANVA-')],
        [sg.HSeparator()],
        [sg.Text("CP",font=('Helvetica',15)),sg.Listbox(values=["NG","OK"],font=('Helvetica',15),size=(5,1)),sg.Text("\tBFC",font=('Helvetica',15)),sg.Listbox(values=["NG","OK"],font=('Helvetica',15),size=(5,1)),sg.Push(),sg.Text("Observaciones:\t\t",font=('Helvetica',15,'bold')),sg.Push()],
        [sg.Text("QP",font=('Helvetica',15)),sg.Listbox(values=["NG","OK"],font=('Helvetica',15),size=(5,1)),sg.Text("\tHOVER",font=('Helvetica',15)),sg.Listbox(values=["NG","OK"],font=('Helvetica',15),size=(5,1)),sg.Push(),sg.Multiline("" ,size=(50 ,5) ,no_scrollbar=True ,enable_events=True),sg.Push()],
        ]
    
    # layout_inf = [
    #     [sg.Text('--------------------------------------------------------------------------------------------------------------------------------',font=('Helvetica',15,'bold'))],
    #     [sg.Text("CP"),sg.Text("")]
    # ]
   
    # layout=[
    # [sg.Column(layout_sup)],
    # [sg.HSeparator()],
    # [sg.Column(layout_inf)],  # sg.vtop para tomar toda la columna y recorrerla hacia arriba
    # ] 
    
    
    
    window = sg.Window('Manto Feeder Main', layout,element_justification='center')
    while True:
        event, values = window.read()
        #print(event, values)
        if event == sg.WIN_CLOSED:
            break
        
        if event == 'test':
            print("Conexion!")
        
    window.close()
    
if __name__ == '__main__':
    app()