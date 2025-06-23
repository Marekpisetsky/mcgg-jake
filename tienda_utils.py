import time

import io_backend
from detection import load_detector, is_shop_visible


# Región donde debería verse el botón/área de la tienda. Las coordenadas son
# aproximadas y pueden ajustarse según la resolución utilizada.
SHOP_BUTTON_REGION = (620, 640, 80, 80)

_detector = None


def _ensure_detector():
    global _detector
    if _detector is None:
        _detector = load_detector("detector.pth")


def tienda_presente():
    """Devuelve ``True`` si se detecta el botón de la tienda en pantalla."""
    _ensure_detector()
    try:
        captura = io_backend.screenshot(region=SHOP_BUTTON_REGION)
        if captura is None:
            return False
        return is_shop_visible(_detector, captura)
    except io_backend.ADBError as exc:
        print(f"[ADB ERROR] {exc}")
        return False
    except Exception as exc:
        print(f"[ERROR] No se pudo verificar la tienda: {exc}")
        return False


def abrir_tienda():
    """Envía un atajo de teclado para intentar abrir la tienda."""
    try:
        io_backend.press("b")
    except io_backend.ADBError as exc:
        print(f"[ADB ERROR] {exc}")
    time.sleep(0.5)
