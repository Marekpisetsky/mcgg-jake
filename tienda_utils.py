import time
import pyautogui
from PIL import ImageStat

# Región donde debería verse el botón/área de la tienda. Las coordenadas son
# aproximadas y pueden ajustarse según la resolución utilizada.
SHOP_BUTTON_REGION = (620, 640, 80, 80)


def tienda_presente():
    """Devuelve ``True`` si se detecta el botón de la tienda en pantalla."""
    try:
        captura = pyautogui.screenshot(region=SHOP_BUTTON_REGION)
        brillo = ImageStat.Stat(captura.convert("L")).mean[0]
        return brillo > 30
    except Exception as exc:
        print(f"[ERROR] No se pudo verificar la tienda: {exc}")
        return False


def abrir_tienda():
    """Envía un atajo de teclado para intentar abrir la tienda."""
    pyautogui.press("b")
    time.sleep(0.5)
