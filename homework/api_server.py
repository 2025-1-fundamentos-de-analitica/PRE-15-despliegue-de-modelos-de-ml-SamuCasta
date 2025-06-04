# api_server.py
"""
Servidor API REST para el modelo de predicción de precios de casas.
Este script crea una API que recibe datos JSON y devuelve predicciones.

Ejemplo de uso desde línea de comandos:
curl http://127.0.0.1:5000 -X POST -H "Content-Type: application/json" \
-d '{"bathrooms": "2", "bedrooms": "3", "sqft_living": "1800", \
"sqft_lot": "2200", "floors": "1", "waterfront": "1", "condition": "3"}'

En Windows:
curl http://127.0.0.1:5000 -X POST -H "Content-Type: application/json" -d "{\"bathrooms\": \"2\", \"bedrooms\": \"3\", \"sqft_living\": \"1800\", \"sqft_lot\": \"2200\", \"floors\": \"1\", \"waterfront\": \"1\", \"condition\": \"3\"}"
"""

import pickle

import pandas as pd  # type: ignore
from flask import Flask, request  # type: ignore

# Crear la instancia de la aplicación Flask
app = Flask(__name__)
# Configurar una clave secreta para seguridad de sesiones
app.config["SECRET_KEY"] = "you-will-never-guess"

# Lista de características (features) que el modelo espera recibir
# Esta debe coincidir exactamente con las características usadas durante el entrenamiento
FEATURES = [
    "bedrooms",      # Número de dormitorios
    "bathrooms",     # Número de baños
    "sqft_living",   # Pies cuadrados de espacio habitable
    "sqft_lot",      # Pies cuadrados del lote
    "floors",        # Número de pisos
    "waterfront",    # Vista al agua (0=sí, 1=no)
    "condition",     # Condición de la casa (1-5)
]


@app.route("/", methods=["POST"])
def index():
    """
    Función API que procesa requests POST con datos JSON.
    
    Recibe un JSON con las características de la casa y devuelve
    una predicción del precio como string.
    
    Returns:
        str: Precio predicho como string
    """

    # Obtener los datos JSON del request
    args = request.json
    
    # Filtrar y convertir los argumentos recibidos
    # Crear un diccionario con las características, convertidas a enteros
    # y organizadas como listas para crear un DataFrame
    filt_args = {key: [int(args[key])] for key in FEATURES}
    
    # Convertir el diccionario filtrado a DataFrame
    # El modelo requiere los datos en este formato
    df = pd.DataFrame.from_dict(filt_args)

    # Cargar el modelo entrenado desde el archivo pickle
    with open("homework/house_predictor.pkl", "rb") as file:
        loaded_model = pickle.load(file)

    # Realizar la predicción usando el modelo cargado
    # prediction es un array numpy con la predicción
    prediction = loaded_model.predict(df)

    # Retornar la predicción como string
    # [0][0] accede al primer elemento del array de predicciones
    return str(prediction[0][0])


# Ejecutar la aplicación Flask en modo debug cuando se ejecute directamente
if __name__ == "__main__":
    app.run(debug=True)