import cv2
import pytesseract
import re
import config

if config.IO_MODE == "mobile":
    import mobile_io as io_backend
else:
    import pyautogui as io_backend

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



def detectar_ronda():
    x, y, w, h = 480, 63, 40, 20  # coordenadas pantalla 1366x768
    screenshot = io_backend.screenshot(region=(x, y, w, h))
    screenshot.save("debug_ronda_raw.png")

    imagen = cv2.imread("debug_ronda_raw.png")
    if imagen is None:
        print("⚠️ No se pudo capturar la ronda en pantalla")
        return None

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


