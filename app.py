from types import MethodDescriptorType
from flask import Flask, jsonify, request
from products import products
app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/<name>')
def index(name):
    return '<h1>Hello {}!</h1>'.format(name)

@app.route('/ping')
def ping():
    return jsonify({"message": "Pong!"})

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