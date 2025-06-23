"""Lectura de la ronda usando un detector de objetos."""

import cv2
import pytesseract
import re
import io_backend
import numpy as np

from detection import load_detector, detect


_detector = None

def limpiar_ocr(texto):
    reemplazos = {
        '–': '-', '—': '-', '−': '-',
        '|': 'I', '1': 'I', 'l': 'I', 'L': 'V',
        'VV': 'V',  # Corrige casos como VV-5 → V-5
        '‘': '', '’': '', '“': '', '”': '',
    }
    for k, v in reemplazos.items():
        texto = texto.replace(k, v)
    return texto.strip()



def _ensure_detector():
    global _detector
    if _detector is None:
        _detector = load_detector("detector.pth")


def detectar_ronda():
    _ensure_detector()
    screenshot = io_backend.screenshot()
    resultados = detect(_detector, screenshot, 0.4)
    bbox = next((b for l, b, s in resultados if l == "ronda"), None)
    if bbox is None:
        print("⚠️ No se encontró la región de la ronda")
        return None
    x1, y1, x2, y2 = map(int, bbox)
    imagen = cv2.cvtColor(np.array(screenshot.crop((x1, y1, x2, y2))), cv2.COLOR_RGB2BGR)

    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    binaria = cv2.adaptiveThreshold(gris, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                    cv2.THRESH_BINARY_INV, 11, 2)
    invertida = cv2.bitwise_not(binaria)
    cv2.imwrite("debug_ronda_proc.png", invertida)

    custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=IVXLCDM1234567890-'
    texto = pytesseract.image_to_string(invertida, config=custom_config)
    texto = limpiar_ocr(texto).upper()
    print(f"🧪 OCR detectó: {texto}")

    # Extraer solo la primera coincidencia tipo X-1, I-2, V-3, etc.
    coincidencias = re.findall(r"[IVXLCDM1lL|]{1,4}-[1-6]", texto)
    if coincidencias:
        ronda = limpiar_ocr(coincidencias[0])
        print(f"✅ Ronda detectada: {ronda}")
        return ronda
    else:
        print("❌ No se detectó la ronda.")
        return None


