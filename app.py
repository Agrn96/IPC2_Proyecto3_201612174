from storage import Lista_Simple
from test import cargar_Archivo, procesar
from types import MethodDescriptorType
from flask import Flask, jsonify, request
from flask_cors import CORS
from products import products
import xmltodict, json
import webbrowser
app = Flask(__name__)
CORS(app)

lista = Lista_Simple()

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/<name>')
def index(name):
    return '<h1>Hello {}!</h1>'.format(name)

@app.route('/ping') #Return xml file
def ping():
    cargar_Archivo(lista)
    ruta = "./env/Lib/site-packages/django/contrib/auth/templates/Salida.xml"
    file1 = open(ruta,'r')
    lines = file1.readlines()
    hold = ""
    for line in lines:
        hold += str(line)
    temp = {'xml':hold}
    return jsonify(temp)

@app.route('/graph1/<string:fecha>') #DATE and USERS
def graph1(fecha):
    ruta = "./env/Lib/site-packages/django/contrib/auth/templates/Salida.xml"
    with open(ruta, 'r') as myfile:
        obj = xmltodict.parse(myfile.read())
    temp_ = str(fecha[8]) +  str(fecha[9]) + "/" + str(fecha[5]) +  str(fecha[6]) +  "/" + str(fecha[0]) + str(fecha[1]) + str(fecha[2]) + str(fecha[3])
    print(temp_)
    
    x = []
    y = []
    for date in obj['ESTADISTICAS']['ESTADISTICA']:
        if(str(date['FECHA']) == str(temp_)):
            #print(date)
            #print(date['REPORTADO_POR']['USUARIO'][0]['EMAIL'])
            for user in date['REPORTADO_POR']['USUARIO']:
                    x.append(user['EMAIL'])
                    y.append(user['CANTIDAD_MENSAJES'])
    return jsonify({'x':x, 'y':y})

@app.route('/graph2/<string:fecha>') #DATE and ERRORS
def graph2(fecha):
    ruta = "./env/Lib/site-packages/django/contrib/auth/templates/Salida.xml"
    with open(ruta, 'r') as myfile:
        obj = xmltodict.parse(myfile.read())
    temp_ = str(fecha[8]) +  str(fecha[9]) + "/" + str(fecha[5]) +  str(fecha[6]) +  "/" + str(fecha[0]) + str(fecha[1]) + str(fecha[2]) + str(fecha[3])
    print(temp_)
    
    x = []
    y = []
    for date in obj['ESTADISTICAS']['ESTADISTICA']:
        if(str(date['FECHA']) == temp_):
            print(date)
            print(date['REPORTADO_POR']['USUARIO'][0]['EMAIL'])
            for user in date['ERRORES']['AFECTADO']:
                    x.append(user['CODIGO'])
                    y.append(user['CANTIDAD_MENSAJES'])

    return jsonify({'x':x, 'y':y})

@app.route('/reset')
def reset():
    ruta = "./env/Lib/site-packages/django/contrib/auth/templates/Salida.xml"
    with open(ruta, 'w') as myfile:
        myfile.write("")
    myfile.close()

@app.route('/info')
def info():
    ruta = "ArticuloEnsayo-IPC2.pdf"
    webbrowser.open(ruta)

@app.route('/products')
def getProducts():
    return jsonify({"products": products, "message":"Product's List"})

@app.route('/products/<string:p_name>')
def getProduct(p_name):
    productsFound = [product for product in products if product['name'] == p_name]
    if(len(productsFound) > 0):
        return jsonify({"product":productsFound[0]})
    return jsonify({"message": "Product not found"})

@app.route('/products', methods=['POST'])
def addProduct():
    new_product = {
        "name": request.json['name'],
        "price": request.json['price'],
        "quantity": request.json['quantity']
    }
    products.append(new_product)
    return jsonify({"message":"Product Added Successfully", "Products": products})

@app.route('/products/<string:product_name>', methods=['PUT'])
def editProduct(product_name):
    productFound = [product for product in products if product['name'] == product_name]
    if (len(productFound) > 0):
        productFound[0]['name'] = request.json['name']
        productFound[0]['price'] = request.json['price']
        productFound[0]['quantity'] = request.json['quantity']
        return jsonify({
            "message": "Product Updated",
            "product": productFound[0]
        })
    return jsonify({"message": "Product not Found"})