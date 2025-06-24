import io_backend
from detection import load_detector, detect_level

_detector = None


def _ensure_detector():
    global _detector
    if _detector is None:
        _detector = load_detector("detector.pth")


def detectar_nivel():
    _ensure_detector()
    captura = io_backend.screenshot()
    if captura is None:
        return None
    return detect_level(_detector, captura, 0.4)


if __name__ == "__main__":
    nivel = detectar_nivel()
    print("Nivel detectado:", nivel)
