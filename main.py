from flask import Flask, render_template, request, redirect, url_for
import matplotlib.pyplot 
matplotlib.use('Agg')
import requests, matplotlib.pyplot as plt, io, base64
from collections import defaultdict

app = Flask(__name__)

API_URL = "http://127.0.0.1:5000"

#Registrar un crédito
@app.route('/creditos/registrar', methods=['GET','POST'])
def mostrar_formulario():
    if request.method == "GET":
        return render_template('formulario_registro_credito.html') 
    else: 
        datos = {
            'cliente': request.form['cliente'],
            'monto': request.form['monto'],
            'tasa_interes': request.form['tasa_interes'],
            'plazo': request.form['plazo'],
            'fecha_otorgamiento': request.form['fecha_otorgamiento']
        }
        response = requests.post(f"{API_URL}/creditos/registrar", json=datos)
        if response.status_code == 200:
            return redirect(url_for('inicio',success='true'))  
        else:
            return "Error al registrar el crédito", 400

#Editar un crédito
@app.route('/creditos/editar/<id>', methods=['GET','POST'])
def editar_credito(id):
    if request.method == 'GET':
        url = f"{API_URL}/credito/{id}"
        api_creditos = requests.get(url)
        data_api = api_creditos.json()
        print(data_api)
        return render_template('formulario_editar_credito.html', data=data_api)
    else:
        datos = {
            'id' : id,
            'cliente': request.form['cliente'],
            'monto': request.form['monto'],
            'tasa_interes': request.form['tasa_interes'],
            'plazo': request.form['plazo'],
            'fecha_otorgamiento': request.form['fecha_otorgamiento']
        }
        response = requests.put(f"{API_URL}/creditos/editar/{id}", json=datos)
        if response.status_code == 200:
            return redirect(url_for('inicio', success='true'))
        else:
            return "Error al editar el crédito", 400
 
#Eliminar un crédito       
@app.route('/creditos/eliminar/<id>', methods=['POST'])
def eliminar_credito(id):
    response = requests.delete(f"{API_URL}/creditos/eliminar/{id}")
    if response.status_code == 200:
        return redirect(url_for('inicio', success='true'))
    else:
        return "Error al eliminar el crédito", 400

#Visualizar todos los créditos
@app.route('/')
def inicio():
    success = request.args.get('success')
    url = f"{API_URL}/creditos"
    api_creditos = requests.get(url)
    data_api = api_creditos.json()
    return render_template('index.html', data=data_api, success=success)

#Visualizar los detalles de un crédito
@app.route('/credito/<id>', methods=['GET'])
def ver_credito(id):
    url = f"{API_URL}/credito/{id}" 
    api_creditos = requests.get(url)
    data_api = api_creditos.json()
    return render_template('credito.html', data=data_api)


@app.route('/creditos/graficas')
def ver_graficas():
    url = requests.get(f"{API_URL}/creditos")
    creditos = url.json()

    if not creditos:
        return render_template('graficas.html', error="No hay datos de créditos para mostrar")
    
    
    clientes = [c[1] for c in creditos]
    montos = [c[2] for c in creditos]
    fechas = [c[5] for c in creditos] 

    # hacer el conteo de los créditos por fecha
    creditos_por_fecha = defaultdict(int)
    for fecha in fechas:
        creditos_por_fecha[fecha] += 1
    
    fechas_ordenadas = sorted(creditos_por_fecha.keys())
    conteos = [creditos_por_fecha[fecha] for fecha in fechas_ordenadas]
    
    # Obtener el total de creditos según el rango del monto
    rangos = ['0-1000', '1001-5000', '5001-10000', '10001+']
    conteo_rangos = [0] * len(rangos)
    for monto in montos:
        if monto <= 1000:
            conteo_rangos[0] += 1
        elif monto <= 5000:
            conteo_rangos[1] += 1
        elif monto <= 10000:
            conteo_rangos[2] += 1
        else:
            conteo_rangos[3] += 1

    graphics = []
    
    # Gráfica 1: Montos por cliente
    fig1 = plt.figure(figsize=(10, 6))
    plt.bar(clientes, montos)
    plt.title('Montos de créditos por cliente')
    plt.xlabel('Clientes')
    plt.ylabel('Monto')
    plt.xticks(rotation=45)
    plt.tight_layout()
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graphics.append(base64.b64encode(buffer.getvalue()).decode('utf-8'))
    buffer.close()
    plt.close(fig1)
    
    # Gráfica 2: Créditos por fecha
    fig2 = plt.figure(figsize=(10, 6))
    plt.bar(fechas_ordenadas, conteos)
    plt.title('Total de créditos por fecha de otorgamiento')
    plt.xlabel('Fecha')
    plt.ylabel('Número de Créditos')
    plt.xticks(rotation=45)
    plt.tight_layout()
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graphics.append(base64.b64encode(buffer.getvalue()).decode('utf-8'))
    buffer.close()
    plt.close(fig2)
    
    # Gráfica 3: Créditos por rango de monto
    fig3=plt.figure(figsize=(10, 6))
    plt.bar(rangos, conteo_rangos)
    plt.title('Distribución de créditos por rango de monto')
    plt.xlabel('Rango de Monto')
    plt.ylabel('Número de Créditos')
    plt.tight_layout()
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graphics.append(base64.b64encode(buffer.getvalue()).decode('utf-8'))
    buffer.close()
    plt.close(fig3)
    
    return render_template('graficas.html', 
                         graphic=graphics[0],  # Montos por cliente
                         graphic2=graphics[1], # Créditos por fecha
                         graphic3=graphics[2], # Créditos por rango
                        ) 

if __name__ == '__main__':
    
    app.run(port=5001, debug=True)