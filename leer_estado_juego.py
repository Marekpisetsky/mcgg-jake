# leer_estado_juego.py

from leer_ronda_automatica import detectar_ronda as obtener_ronda
from leer_oro_automatico import detectar_oro
from detectar_sinergias import detectar_sinergias_activas
from detection import load_detector, detect_heroes, detect_level
import io_backend
import os
import logging

logging.basicConfig(level=logging.INFO)

_detector = None
_detector_mtime = None


def _ensure_detector():
    global _detector, _detector_mtime
    try:
        mtime = os.path.getmtime("detector.pth")
    except OSError:
        mtime = None
    if _detector is None or mtime != _detector_mtime:
        _detector = load_detector("detector.pth")
        _detector_mtime = mtime


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
        logging.error("[ERROR] No se pudo leer la ronda: %s", e)

    try:
        sinergias = detectar_sinergias_activas()
        estado["sinergias"] = sinergias
    except Exception as e:
        estado["sinergias"] = []
        logging.error("[ERROR] No se pudo leer las sinergias: %s", e)

    try:
        oro = detectar_oro()
        estado["oro"] = oro
    except Exception as e:
        estado["oro"] = None
        logging.error("[ERROR] No se pudo leer el oro: %s", e)

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
        logging.error("[ERROR] No se pudieron detectar tienda/banco: %s", e)

    return estado


# Prueba directa
if __name__ == "__main__":
    estado = leer_estado_juego()
    logging.info("Estado actual del juego: %s", estado)
