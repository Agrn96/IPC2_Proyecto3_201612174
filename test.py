import xml.etree.ElementTree as ET
from tkinter import *
from tkinter import filedialog

def cargar_Archivo():
    filename = filedialog.askopenfile(filetypes=(('text files', 'xml'),))
    #tree = ET.parse(filename)       
    #root = tree.getroot()        
    #agregar informacion en Listas
    #for nombre in root:
    #    print(nombre)
    print(filename)

cargar_Archivo()