import xmltodict, json

def test(): #Date and users reported
    ruta = "./env/Lib/site-packages/django/contrib/auth/templates/Salida.xml"
    with open(ruta, 'r') as myfile:
        obj = xmltodict.parse(myfile.read())
    temp_ = "15/01/2021"
    print(temp_)
    x = []
    y = []
    for date in obj['ESTADISTICAS']['ESTADISTICA']:
        print(date)
        if(date['FECHA'] == temp_):
            print(date)
            print(date['REPORTADO_POR']['USUARIO'][0]['EMAIL'])
            for user in date['ERRORES']['AFECTADO']:
                    x.append(user['CODIGO'])
                    y.append(user['CANTIDAD_MENSAJES'])
            break
    print(x)
    print('---')
    print(y)
test()

#['EMAIL']['CANTIDAD_MENSAJES'] print(date['REPORTADO_POR']['USUARIO'][0]['EMAIL'])