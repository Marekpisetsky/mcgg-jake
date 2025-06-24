import cv2
import numpy as np
import pytesseract
from config import FIN_PARTIDA_REGION, EXIT_BUTTON_REGION


    # El botón "Salir" puede aparecer si seguimos observando tras perder.
    x, y, w, h = EXIT_BUTTON_REGION
    region = captura.crop((x, y, x + w, y + h))
    gray = cv2.cvtColor(np.array(region), cv2.COLOR_RGB2GRAY)
    texto = pytesseract.image_to_string(gray, config="--psm 7").lower()
    if any(p in texto for p in ("salir", "exit")):
        # No se puede saber el resultado exacto; asumimos fin sin marcador.
        return True, None

import io_backend
from config import FIN_PARTIDA_REGION


def detectar_fin_partida() -> tuple[bool, bool | None]:
    """Return ``(fin, gano)`` based on OCR of the result text.
    ``fin`` indica si se detectó la pantalla de fin de partida.
    ``gano`` es ``True`` si se detecta una victoria, ``False`` si se detecta una
    derrota y ``None`` en caso de que no se pueda determinar.
    """
    captura = io_backend.screenshot()
    if captura is None:
        return False, None

    x, y, w, h = FIN_PARTIDA_REGION
    region = captura.crop((x, y, x + w, y + h))
    gray = cv2.cvtColor(np.array(region), cv2.COLOR_RGB2GRAY)
    texto = pytesseract.image_to_string(gray, config="--psm 7").lower()
    if any(p in texto for p in ("victory", "victoria")):
        return True, True
    if any(p in texto for p in ("defeat", "derrota")):
        return True, False
    return False, None
