import pyautogui
import pytesseract
from PIL import Image
import cv2
import numpy as np
import time

def leer_oro_desde_imagen(ruta):
    import cv2
    import pytesseract
    import numpy as np

    imagen = cv2.imread(ruta)
    
    # Aumentar tamaño
    imagen = cv2.resize(imagen, None, fx=5, fy=5, interpolation=cv2.INTER_CUBIC)
    
    # Convertir a escala de grises
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Aplicar blur ligero para eliminar artefactos
    gris = cv2.medianBlur(gris, 3)

    # Umbral binario directo (sin inversión)
    _, binaria = cv2.threshold(gris, 160, 255, cv2.THRESH_BINARY)

    # OCR solo con dígitos permitidos
    config = "--psm 8 -c tessedit_char_whitelist=0123456789"
    texto = pytesseract.image_to_string(binaria, config=config)

    return texto.strip()



def capturar_y_leer_oro():
    # Coordenadas del centro del número (ajusta según tu pantalla)
    x, y, w, h = 1205, 580, 80, 40  # <-- Ajusta estos valores
    captura = pyautogui.screenshot(region=(x, y, w, h))
    ruta_imagen = "frame_oro.png"
    captura.save(ruta_imagen)
    print("[✓] Captura guardada en:", ruta_imagen)
    
    texto = leer_oro_desde_imagen(ruta_imagen)
    if texto.isdigit():
        print("[✔] Oro detectado:", texto)
    else:
        print("[✘] No se detectó ningún número.")

if __name__ == "__main__":
    capturar_y_leer_oro()
