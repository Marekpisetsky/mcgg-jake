"""Lectura automática del oro usando un detector de objetos."""

import io_backend
import pytesseract
from PIL import Image
import cv2
import numpy as np

from detection import load_detector, detect


_detector = None



def leer_oro_desde_imagen(imagen_or_ruta):
    """Return the detected gold amount from an image or image path."""
    if isinstance(imagen_or_ruta, Image.Image):
        imagen = cv2.cvtColor(np.array(imagen_or_ruta), cv2.COLOR_RGB2BGR)
    else:
        imagen = cv2.imread(imagen_or_ruta)
    
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



def _ensure_detector():
    global _detector
    if _detector is None:
        _detector = load_detector("detector.pth")


def capturar_y_leer_oro():
    """Captura la pantalla completa y detecta la región del oro."""
    _ensure_detector()
    captura = io_backend.screenshot()
    if captura is None:
        return None
    resultados = detect(_detector, captura, 0.4)
    bbox = next((b for l, b, s in resultados if l == "oro"), None)

    if bbox is None:
        print("[✘] No se encontró la región de oro")
        return None

    x1, y1, x2, y2 = map(int, bbox)
    region = captura.crop((x1, y1, x2, y2))

    texto = leer_oro_desde_imagen(region)
    if texto.isdigit():
        print("[✔] Oro detectado:", texto)
        return int(texto)
    print("[✘] No se detectó ningún número.")
    return None


def detectar_oro():
    """Captura la zona de oro y devuelve el valor detectado.

    Esta función actúa como un pequeño wrapper para ``capturar_y_leer_oro`` pero
    retornando únicamente el número obtenido en lugar de imprimirlo por
    pantalla.
    """
    valor = capturar_y_leer_oro()
    return valor

if __name__ == "__main__":
    capturar_y_leer_oro()
