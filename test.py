import xml.etree.ElementTree as ET
from tkinter import *
from tkinter import filedialog
import re
import codecs
import xmltodict, json

def cargar_Archivo(lista):
    with codecs.open(filedialog.askopenfilename(filetypes=[("Text files","*.xml")]), encoding='utf-8') as filename:
        procesar(filename, lista)
    filename.close()

def procesar(filename, lista):
    dateRegex = re.compile(r'(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d')
    emailRegex = re.compile(r'([\w|-|\.]+@([\w-]+\.)+[\w-]{2,4})')
    errorRegex = re.compile(r'([0-9]{5})')

    fecha = ""
    user_Reported = ""
    users_Affected = set([])
    errorCode = ""
    errorDesc = ""

    state = 0
    codeFound = 0
    for line in filename:#print(state)
        line = line[:-2]
        line = line.replace("\t","")
        if(line[0] == " "):
            line = line[1:]#print(line)
        if(state == 0):
            fecha = ""              #Resetting temporary holders
            user_Reported = ""
            users_Affected = set([])
            errorCode = ""
            errorDesc = ""
            if(line.find("<EVENTOS>") != -1):
                state = 0
                continue
            elif(line.find("<EVENTO>") != -1):
                state = 1
            elif(line.find("</EVENTOS>") != -1):
                break
        elif(state == 1): #1st line collect date
            if(dateRegex.search(line)):
                fecha_ = dateRegex.search(line)
                fecha += fecha_.group(0)#print(fecha_.group(0))
                state = 2
            else:
                print("failed state 0")
                state = 0
        elif(state == 2): # 2nd line collect user
            if(emailRegex.search(line)):
                correo = emailRegex.search(line)
                user_Reported += correo.group(0)#print(correo.group(0))
                state = 3
            else:
                print("failed state 1")
                state = 0
        elif(state == 3): # 3rd line, collect affected users
            if(emailRegex.search(line)):
                correo = emailRegex.findall(line)#print(correo) #To get the email, use array [x][0] and add it to memory
                for item in correo:
                    users_Affected.add(item[0])
                state = 4
            else:
                print("failed state 2")
                state = 0
        elif(state == 4): # 4th line, collect error
            if(line.find('</EVENTO') != -1):
                lista.add(fecha,user_Reported,users_Affected,errorCode,errorDesc)
                state = 0
                codeFound = 0
                continue
            if(errorRegex.search(line) and codeFound == 0):
                errorCode_ = errorRegex.search(line)
                errorCode = errorCode_.group(0)#print(errorCode_.group(0))
                hold = line.split('-')
                errorDesc_ = hold[1]
                if(errorDesc_[0] == " "):
                    errorDesc += errorDesc_[1:]#print(errorDesc)
                codeFound = 1
            else:
                line = line.replace("\t","")
                errorDesc += " " + line#print(errorDesc)
    
    generar_Salida(lista)

def generar_Salida(lista):
    temp = lista.head
    root = ET.Element("ESTADISTICAS")
    while(temp != None):
        matriz = ET.SubElement(root, "ESTADISTICA")
        ET.SubElement(matriz, "FECHA").text = str(temp.fecha)
        ET.SubElement(matriz, "CANTIDAD_MENSAJES").text = str(temp.reports)
        report = ET.SubElement(matriz, "REPORTADO_POR")
        for key,value in temp.users_R.items():
            user = ET.SubElement(report, "USUARIO")
            ET.SubElement(user, "EMAIL").text = str(key)
            ET.SubElement(user, "CANTIDAD_MENSAJES").text = str(value)
        afectados = ET.SubElement(matriz, "AFECTADOS")
        for key in temp.users_A:
            user = ET.SubElement(afectados, "AFECTADO").text = str(key)
        errores = ET.SubElement(matriz, "ERRORES")
        for key,value in temp.error.items():
            user = ET.SubElement(errores, "AFECTADO")
            ET.SubElement(user, "CODIGO").text = str(key)
            ET.SubElement(user, "CANTIDAD_MENSAJES").text = str(value)
        temp = temp.next

    prettify(root)
    tree = ET.ElementTree(root)
    ruta = "./env/Lib/site-packages/django/contrib/auth/templates/Salida.xml"
    tree.write(ruta, encoding='UTF-8', xml_declaration=False)
    # Create json file
    with open(ruta, 'r') as myfile:
        obj = xmltodict.parse(myfile.read())
    print(json.dumps(obj))


def prettify(element, indent='  '):
    queue = [(0, element)]  # (level, element)
    while queue:
        level, element = queue.pop(0)
        children = [(level + 1, child) for child in list(element)]
        if children:
            element.text = '\n' + indent * (level+1)  # for child open
        if queue:
            element.tail = '\n' + indent * queue[0][0]  # for sibling open
        else:
            element.tail = '\n' + indent * (level-1)  # for parent close
        queue[0:0] = children  # prepend so children come before siblings

def procesar_(filename, lista):
    dateRegex = re.compile(r'(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d')
    emailRegex = re.compile(r'([\w|-|\.]+@([\w-]+\.)+[\w-]{2,4})')
    errorRegex = re.compile(r'([0-9]{5})')

    fecha = ""
    user_Reported = ""
    users_Affected = set([])
    errorCode = ""
    errorDesc = ""

    state = 0
    codeFound = 0
    for line in filename:#print(state)
        line = line[:-2]
        line = line.replace("\t","")
        if(line[0] == " "):
            line = line[1:]#print(line)
        if(state == 0):
            fecha = ""              #Resetting temporary holders
            user_Reported = ""
            users_Affected = set([])
            errorCode = ""
            errorDesc = ""
            if(line.find("<EVENTOS>") != -1):
                state = 0
                continue
            elif(line.find("<EVENTO>") != -1):
                state = 1
            elif(line.find("</EVENTOS>") != -1):
                break
        elif(state == 1): #1st line collect date
            if(dateRegex.search(line)):
                fecha_ = dateRegex.search(line)
                fecha += fecha_.group(0)#print(fecha_.group(0))
                state = 2
            else:
                print("failed state 0")
                state = 0
        elif(state == 2): # 2nd line collect user
            if(emailRegex.search(line)):
                correo = emailRegex.search(line)
                user_Reported += correo.group(0)#print(correo.group(0))
                state = 3
            else:
                print("failed state 1")
                state = 0
        elif(state == 3): # 3rd line, collect affected users
            if(emailRegex.search(line)):
                correo = emailRegex.findall(line)#print(correo) #To get the email, use array [x][0] and add it to memory
                for item in correo:
                    users_Affected.add(item[0])
                state = 4
            else:
                print("failed state 2")
                state = 0
        elif(state == 4): # 4th line, collect error
            if(line.find('</EVENTO') != -1):
                lista.add(fecha,user_Reported,users_Affected,errorCode,errorDesc)
                state = 0
                codeFound = 0
                continue
            if(errorRegex.search(line) and codeFound == 0):
                errorCode_ = errorRegex.search(line)
                errorCode = errorCode_.group(0)#print(errorCode_.group(0))
                hold = line.split('-')
                errorDesc_ = hold[1]
                if(errorDesc_[0] == " "):
                    errorDesc += errorDesc_[1:]#print(errorDesc)
                codeFound = 1
            else:
                line = line.replace("\t","")
                errorDesc += " " + line#print(errorDesc)