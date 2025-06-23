import cv2
import json
import os
import config

if config.IO_MODE == "mobile":
    import mobile_io as io_backend
else:
    import pyautogui as io_backend

X_BASE = 5
Y_BASE = 180
ANCHO = 35
ALTO = 35
ESPACIADO_Y = 45
NUM_ICONOS = 19

def cargar_etiquetas(path="sinergias.json"):
    if not os.path.exists(path):
        return {str(i): f"sinergia_{i}" for i in range(NUM_ICONOS)}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def detectar_sinergias_activas():
    etiquetas = cargar_etiquetas()
    activas = []

    for i in range(NUM_ICONOS):
        x = X_BASE
        y = Y_BASE + i * ESPACIADO_Y

        captura = io_backend.screenshot(region=(x, y, ANCHO, ALTO))
        nombre_debug = f"debug_sinergia_{i}.png"
        captura.save(nombre_debug)

        img = cv2.imread(nombre_debug)
        if img is None:
            continue

        gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gris, 200, 255, cv2.THRESH_BINARY)
        porcentaje_blanco = (cv2.countNonZero(mask) / (ANCHO * ALTO)) * 100

        if porcentaje_blanco > 4:
            activas.append(etiquetas.get(str(i), f"sinergia_{i}"))

    return activas
