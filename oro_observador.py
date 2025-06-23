# oro_observador.py
import pytesseract
import cv2
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

CARPETA = "oro_recolectado"

def detectar_y_guardar(path="frame_oro.png"):
    if not os.path.exists(CARPETA):
        os.makedirs(CARPETA)

    img = cv2.imread(path)
    img = cv2.resize(img, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, tresh = cv2.threshold(gris, 170, 255, cv2.THRESH_BINARY)

    config = r'--psm 8 -c tessedit_char_whitelist=0123456789'
    texto = pytesseract.image_to_string(tresh, config=config).strip()
    texto = texto.replace('\n', '').replace('\f', '')

    if texto.isdigit() and 0 <= int(texto) <= 999:
        archivo = os.path.join(CARPETA, f"{texto}.png")
        cv2.imwrite(archivo, cv2.imread(path))
        print(f"[✓] Guardado como {archivo}")
    else:
        print("[✗] OCR poco confiable, ignorado.")

if __name__ == "__main__":
    detectar_y_guardar()
