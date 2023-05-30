import openpyxl
from openpyxl import workbook
from openpyxl.styles import Font, Alignment, Border, Side

def create_template():
    '''
    Funcionamiento basico:
        - Cargar el archivo Excel existente(MF-64_plantilla.XLS)
        - lo convertimos a XLSX(MF-64_plantilla.xlsx)
        ** version mas actual de archivos excel
        -recabamos toda la info de los parametros y generamos una plantilla para guardar como reporte
    parametros(no definidos en funcion aun):
        -Nombre del tecnico
        -ID feeder
        -Tipo de feeder
        -Fecha de mantenimiento
        -Color de semana
    '''
    return create_template.__doc__
    
print(create_template())