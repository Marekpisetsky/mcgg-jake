import cv2
import numpy as np
import pytesseract

import io_backend

# Approximate region where the 'Victory' or 'Defeat' text appears
# Coordinates: (x, y, width, height) for an 800x360 screenshot
FIN_PARTIDA_REGION = (250, 100, 300, 80)


def detectar_fin_partida() -> bool:
    """Return True if the end-of-game screen is detected."""
    captura = io_backend.screenshot()
    if captura is None:
        return False

    x, y, w, h = FIN_PARTIDA_REGION
    region = captura.crop((x, y, x + w, y + h))
    gray = cv2.cvtColor(np.array(region), cv2.COLOR_RGB2GRAY)
    texto = pytesseract.image_to_string(gray, config="--psm 7").lower()
    return any(palabra in texto for palabra in ("victory", "defeat", "victoria", "derrota"))
