import PySimpleGUI as sg

def main():
    layout = [
        [sg.Text('Ingresa un dato:'), sg.Input(key='-INPUT-')],
    ]

    window = sg.Window('Mi aplicación', layout, return_keyboard_events=True)
    #return_keyboard_events=True para que se pueda leer las pulsaciones del teclado
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == '\r':  # Verifica si se presionó la tecla "Enter"
            dato = values['-INPUT-']
            # Aquí puedes colocar el bloque de código que deseas ejecutar
            print(f'Dato ingresado: {dato}')
    
    window.close()

if __name__ == '__main__':
    main()
