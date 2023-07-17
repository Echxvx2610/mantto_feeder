from openpyxl import Workbook
from openpyxl.drawing.image import Image

libro = Workbook()
hoja = libro.active
img = Image('mantto_feeder\img\loggin.png')
hoja.add_image(img, 'B2')

libro.save('mantto_feeder\data\loggin.xlsx')
