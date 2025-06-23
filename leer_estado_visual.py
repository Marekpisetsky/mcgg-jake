from PIL import Image, ImageEnhance
import pytesseract

def leer_numero_oro(ruta_imagen="frame_oro.png"):
    # Abrir imagen original
    imagen = Image.open(ruta_imagen)

    # Recorte manual (ajustado a tu imagen actual)
    # (left, top, right, bottom) — puedes ajustar si lo necesitas
    recorte = imagen.crop((57, 25, 85, 50))

    # Convertir a escala de grises
    gris = recorte.convert("L")

    # Aumentar contraste
    contraste = ImageEnhance.Contrast(gris).enhance(3.0)

    # Redimensionar para facilitar lectura
    ampliada = contraste.resize((contraste.width * 3, contraste.height * 3), Image.BICUBIC)

    # Realizar OCR forzando sólo dígitos
    texto = pytesseract.image_to_string(ampliada, config='--psm 7 -c tessedit_char_whitelist=0123456789')

    # Limpieza de salida
    texto = texto.strip()

    # Mostrar resultado
    if texto.isdigit():
        print(f"[✔] Número detectado: {texto}")
        return int(texto)
    else:
        print("[✘] No se detectó ningún número.")
        return None

# Ejecutar
leer_numero_oro()
