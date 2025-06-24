# leer_estado_juego.py

from leer_ronda_automatica import detectar_ronda as obtener_ronda
from leer_oro_automatico import detectar_oro
from detectar_sinergias import detectar_sinergias_activas
from detection import load_detector, detect_heroes, detect_level
import io_backend

_detector = None


def _ensure_detector():
    global _detector
    if _detector is None:
        _detector = load_detector("detector.pth")


def leer_estado_juego():
    """
    Devuelve el estado actual del juego.
    Incluye: ronda, sinergias activas, cantidad de oro y nivel del jugador.
    """
    estado = {}

    try:
        ronda = obtener_ronda()
        estado["ronda"] = ronda
    except Exception as e:
        estado["ronda"] = None
        print(f"[ERROR] No se pudo leer la ronda: {e}")

    try:
        sinergias = detectar_sinergias_activas()
        estado["sinergias"] = sinergias
    except Exception as e:
        estado["sinergias"] = []
        print(f"[ERROR] No se pudo leer las sinergias: {e}")

    try:
        oro = detectar_oro()
        estado["oro"] = oro
    except Exception as e:
        estado["oro"] = None
        print(f"[ERROR] No se pudo leer el oro: {e}")

    # Detectar héroes en tienda y banco
    try:
        _ensure_detector()
        captura = io_backend.screenshot()
        if captura is not None:
            tienda, banco = detect_heroes(_detector, captura, 0.4)
            nivel = detect_level(_detector, captura, 0.4)
            estado["tienda"] = tienda
            estado["banco"] = banco
            estado["nivel"] = nivel
        else:
            estado.setdefault("tienda", [])
            estado.setdefault("banco", [])
            estado.setdefault("nivel", None)
    except Exception as e:
        estado.setdefault("tienda", [])
        estado.setdefault("banco", [])
        estado.setdefault("nivel", None)
        print(f"[ERROR] No se pudieron detectar tienda/banco: {e}")

    return estado


# Prueba directa
if __name__ == "__main__":
    estado = leer_estado_juego()
    print("Estado actual del juego:", estado)
