import os
import cv2
import numpy as np
from sklearn.neural_network import MLPRegressor
import joblib

def cargar_datos_auto():
    X, y = [], []
    for archivo in os.listdir("datos_oro_auto"):
        if archivo.endswith(".png"):
            path = os.path.join("datos_oro_auto", archivo)
            img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            img = cv2.resize(img, (100, 100)).reshape(-1)
            X.append(img)
            try:
                label = int(archivo.split(".")[0])  # ej: 42.png -> 42
                y.append(label)
            except:
                continue
    return np.array(X), np.array(y)

def entrenar():
    X, y = cargar_datos_auto()
    modelo = MLPRegressor(hidden_layer_sizes=(128,), max_iter=500)
    modelo.fit(X, y)
    joblib.dump(modelo, "modelo_oro.pkl")
    print("[✓] Modelo actualizado")

if __name__ == "__main__":
    entrenar()
