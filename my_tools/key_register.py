import PySimpleGUI as sg
import keyboard


layout = [[sg.Text("", size=(30, 1), key='-TEXT-')]]

window = sg.Window('Detectar Código de Barras', layout)

def barcode_listener(e):
    barcode = keyboard.read_event(e)
    if barcode.event_type == keyboard.KEY_DOWN:
        # Acción a realizar cuando se detecta un escaneo de código de barras
        if barcode.name == 'enter':  # Se asume que el escaneo del código de barras termina con la tecla Enter
            sg.popup(f'Se escaneó el código de barras: {barcode.sequence}')

keyboard.on_release_key('enter', barcode_listener)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break

window.close()
