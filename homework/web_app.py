# web_app.py
"""
Aplicación web Flask para desplegar el modelo de predicción de precios de casas.
Esta aplicación proporciona una interfaz web donde los usuarios pueden ingresar
las características de una casa y obtener una predicción del precio.
"""

import pickle

import pandas as pd  # type: ignore
from flask import Flask, render_template, request  # type: ignore

# Crear la instancia de la aplicación Flask
app = Flask(__name__)
# Configurar una clave secreta para seguridad de sesiones
app.config["SECRET_KEY"] = "you-will-never-guess"


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=("GET", "POST"))
def index():
    """
    Función principal de la página web que maneja tanto GET como POST requests.
    
    - GET: Muestra el formulario vacío para ingresar datos
    - POST: Procesa los datos del formulario y retorna la predicción
    """

    # Si el método es POST, significa que el usuario envió el formulario
    if request.method == "POST":

        # Diccionario para almacenar los valores ingresados por el usuario
        user_values = {}

        # Leer los valores numéricos de las cajas de texto de la interfaz
        # Convertir a float para el procesamiento del modelo
        user_values["bedrooms"] = float(request.form["bedrooms"])      # Número de dormitorios
        user_values["bathrooms"] = float(request.form["bathrooms"])    # Número de baños
        user_values["sqft_living"] = float(request.form["sqft_living"]) # Pies cuadrados de espacio habitable
        user_values["sqft_lot"] = float(request.form["sqft_lot"])       # Pies cuadrados del lote
        user_values["floors"] = float(request.form["floors"])          # Número de pisos

        # Procesar el valor de waterfront (vista al agua)
        # Convertir la respuesta Yes/No a valores numéricos (0=Sí, 1=No)
        if request.form.get("waterfront") == "Yes":
            user_values["waterfront"] = 0  # Sí tiene vista al agua
        else:
            user_values["waterfront"] = 1  # No tiene vista al agua

        # Procesar el valor de condition (condición de la casa)
        # Valores entre 1 (peor condición) y 5 (mejor condición)
        if request.form.get("condition") == "1":
            user_values["condition"] = 1
        elif request.form.get("condition") == "2":
            user_values["condition"] = 2
        elif request.form.get("condition") == "3":
            user_values["condition"] = 3
        elif request.form.get("condition") == "4":
            user_values["condition"] = 4
        else:
            user_values["condition"] = 5

        # Convertir el diccionario a DataFrame para que el modelo pueda procesarlo
        # El modelo espera los datos en formato DataFrame de pandas
        df = pd.DataFrame.from_dict(user_values, orient="index").T

        # Cargar el modelo entrenado desde el archivo pickle
        with open("homework/house_predictor.pkl", "rb") as file:
            loaded_model = pickle.load(file)

        # Realizar la predicción usando el modelo cargado
        # Redondear el resultado a 2 decimales para mejor presentación
        prediction = round(loaded_model.predict(df)[0][0], 2)

    else:
        # Si es método GET, no hay predicción que mostrar
        prediction = None

    # Renderizar la página HTML con la predicción (si existe)
    return render_template("index.html", prediction=prediction)


# Ejecutar la aplicación Flask en modo debug cuando se ejecute directamente
if __name__ == "__main__":
    app.run(debug=True)