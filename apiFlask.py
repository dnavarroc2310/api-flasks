from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Función para obtener y transformar los datos desde Google Sheets
def obtener_datos_google_sheets():
    url = 'https://docs.google.com/spreadsheets/u/3/d/e/2PACX-1vQARG6YSuhowppqNzLe-fsYUZMAGBgFthDXKucSuUNG9m1sEixKieuMJzNDUj7xfg/pubhtml?gid=1489524441&single=true'

    # Hacemos el GET a la URL
    response = requests.get(url)
    if response.status_code != 200:
        return None

    # Parseamos el HTML con BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    tabla = soup.find('table')

    productos = []

    # Extraemos los datos de las filas de la tabla
    if tabla:
        for fila in tabla.find_all('tr')[1:]:  # Omitir la primera fila (encabezados)
            columnas = fila.find_all('td')
            if len(columnas) >= 4:  # Asegúrate de que hay suficientes columnas
                producto = {
                    'nombre': columnas[0].text.strip(),
                    'precio': columnas[1].text.strip(),
                    'url': columnas[2].text.strip(),
                    'descripcion': columnas[3].text.strip()
                }
                productos.append(producto)

    return productos

# Endpoint de la API
@app.route('/api/productos', methods=['GET'])
def obtener_productos():
    productos = obtener_datos_google_sheets()
    if productos is None:
        return jsonify({'error': 'No se pudo obtener los datos'}), 500

    return jsonify(productos)

if __name__ == '__main__':
    app.run(debug=True)
