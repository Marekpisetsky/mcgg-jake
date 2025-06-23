# captura_pantalla.py
"""Captura de la pantalla enfocándose en la tienda y el oro."""

import io_backend
from detection import load_detector, detect


_detector = None


def _ensure_detector():
    global _detector
    if _detector is None:
        _detector = load_detector("detector.pth")


def _guardar_region(imagen, bbox, nombre):
    if bbox is None:
        print(f"[✘] No se encontró la región de {nombre.split('_')[1]}")
        return
    x1, y1, x2, y2 = map(int, bbox)
    region = imagen.crop((x1, y1, x2, y2))
    region.save(nombre)
    print(f"[✓] {nombre} guardado.")

def capturar_pantalla():
    """Captura la pantalla completa y recorta tienda y oro dinámicamente."""
    _ensure_detector()
    captura = io_backend.screenshot()
    if captura is None:
        print("[✘] No se pudo capturar la pantalla")
        return
    resultados = detect(_detector, captura, 0.4)

    tienda_bbox = next((b for l, b, _ in resultados if l == "tienda"), None)
    oro_bbox = next((b for l, b, _ in resultados if l == "oro"), None)

    _guardar_region(captura, tienda_bbox, "frame_tienda.png")
    _guardar_region(captura, oro_bbox, "frame_oro.png")

if __name__ == "__main__":
    capturar_pantalla()
