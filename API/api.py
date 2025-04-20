from flask import Flask, jsonify, request, render_template
import creditos_controller, requests
from db import create_table

app = Flask(__name__)

@app.route('/creditos', methods=['GET'])
def obtener_creditos():
    creditos = creditos_controller.obtener_creditos()
    return jsonify(creditos)

@app.route('/credito/<id>', methods=['GET'])
def ver_credito(id):
    credito = creditos_controller.ver_credito(id)
    return jsonify(credito)
    
@app.route('/creditos/registrar', methods=['POST'])
def registrar_credito():
    detalles = request.get_json()
    cliente = detalles["cliente"]
    monto = detalles["monto"]
    tasa_interes = detalles["tasa_interes"]
    plazo = detalles["plazo"]
    fecha_otorgamiento = detalles["fecha_otorgamiento"]
    result = creditos_controller.insertar(cliente, monto, tasa_interes, plazo, fecha_otorgamiento)
    return jsonify(result)     

@app.route('/creditos/editar/<id>', methods=['PUT'])
def editar_credito(id):
    detalles = request.get_json()
    id = id
    cliente = detalles["cliente"]
    monto = detalles["monto"]
    tasa_interes = detalles["tasa_interes"]
    plazo = detalles["plazo"]
    fecha_otorgamiento = detalles["fecha_otorgamiento"]
    result = creditos_controller.editar(id, cliente, monto, tasa_interes, plazo, fecha_otorgamiento)
    return jsonify(result)

@app.route('/creditos/eliminar/<id>', methods=['DELETE'])
def eliminar_credito(id):
    result = creditos_controller.eliminar(id)
    return jsonify(result)



if __name__ == '__main__':
    create_table()
    app.run(debug=True)