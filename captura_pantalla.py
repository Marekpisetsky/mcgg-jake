# captura_pantalla.py
import mss
import cv2
import numpy as np

# Áreas ajustadas para resolución 1358x704
AREA_TIENDA = {
    "top": 140,         # subimos el punto de inicio
    "left": 280,
    "width": 800,
    "height": 360        # aumentamos el alto
}

AREA_ORO = {
    "top": 540,
    "left": 1165,
    "width": 140,
    "height": 140
}

def capturar_zona(area, nombre_archivo):
    with mss.mss() as sct:
        captura = sct.grab(area)
        imagen = np.array(captura)
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGRA2BGR)
        cv2.imwrite(nombre_archivo, imagen)
        print(f"[✓] {nombre_archivo} guardado.")

def capturar_pantalla():
    capturar_zona(AREA_TIENDA, "frame_tienda.png")
    capturar_zona(AREA_ORO, "frame_oro.png")

if __name__ == "__main__":
    capturar_pantalla()
