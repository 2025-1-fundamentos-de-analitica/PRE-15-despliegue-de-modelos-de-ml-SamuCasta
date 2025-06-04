# train_model.py
"""
Script para entrenar un modelo de regresión lineal para predecir precios de casas.
Este script carga los datos, entrena el modelo y lo guarda para uso posterior.
"""

import pickle

import pandas as pd  # type: ignore
from sklearn.linear_model import LinearRegression  # type: ignore

# Cargar los datos desde el archivo CSV
# Los datos contienen información sobre casas incluyendo características y precios
df = pd.read_csv("files/input/house_data.csv", sep=",")

# Seleccionar las características (features) que se utilizarán para la predicción
# Estas son las variables independientes del modelo
features = df[
    [
        "bedrooms",      # Número de dormitorios
        "bathrooms",     # Número de baños
        "sqft_living",   # Pies cuadrados de espacio habitable
        "sqft_lot",      # Pies cuadrados del lote
        "floors",        # Número de pisos
        "waterfront",    # Si tiene vista al agua (1) o no (0)
        "condition",     # Condición de la casa (escala 1-5)
    ]
]

# Seleccionar la variable objetivo (target) que queremos predecir
# Esta es la variable dependiente del modelo
target = df[["price"]]

# Crear una instancia del modelo de regresión lineal
estimator = LinearRegression()

# Entrenar el modelo con los datos de características y precios
# El modelo aprende la relación entre las características y los precios
estimator.fit(features, target)

# Guardar el modelo entrenado en un archivo usando pickle
# Esto permite reutilizar el modelo sin necesidad de reentrenarlo
with open("homework/house_predictor.pkl", "wb") as file:
    pickle.dump(estimator, file)


