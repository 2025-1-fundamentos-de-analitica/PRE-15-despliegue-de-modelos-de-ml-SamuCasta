# api_client.py
"""
Cliente API para probar el servidor de predicción de precios de casas.
Este script envía una solicitud POST al servidor API y muestra la respuesta.

También se puede usar curl desde línea de comandos:
curl http://127.0.0.1:5000 -X POST -H "Content-Type: application/json" \
-d '{"bathrooms": "2", "bedrooms": "3", "sqft_living": "1800", \
"sqft_lot": "2200", "floors": "1", "waterfront": "1", "condition": "3"}'
"""

import requests  # Para realizar solicitudes HTTP


def make_request():
    """
    Función que realiza una solicitud POST al servidor API.
    
    Envía datos de ejemplo de una casa y recibe la predicción del precio.
    Los datos incluyen todas las características necesarias para la predicción.
    """

    # URL del servidor API local
    url = "http://127.0.0.1:5000"

    # Datos de ejemplo de una casa para la predicción
    # Todos los valores deben ser strings según el formato esperado por la API
    data = {
        "bathrooms": "2",      # 2 baños
        "bedrooms": "3",       # 3 dormitorios
        "sqft_living": "1800", # 1800 pies cuadrados de espacio habitable
        "sqft_lot": "2200",    # 2200 pies cuadrados de lote
        "floors": "1",         # 1 piso
        "waterfront": "1",     # Sin vista al agua (1=no, 0=sí)
        "condition": "3",      # Condición 3 (escala 1-5)
    }

    # Realizar la solicitud POST al servidor
    # - json=data: Envía los datos como JSON
    # - timeout=5: Tiempo límite de 5 segundos para la respuesta
    response = requests.post(url, json=data, timeout=5)

    # Mostrar la respuesta del servidor (predicción del precio)
    print(response.text)


# Ejecutar la función cuando se ejecute el script directamente
if __name__ == "__main__":
    make_request()