# autoetiquetar_oro.py
import shutil
import os
from predecir_oro import predecir

DESTINO = "oro_dataset"
UMBRAL_CONFIANZA = 0.98  # puedes bajarlo a 0.95 si quieres más ejemplos

def autoetiquetar(path="frame_oro.png"):
    pred, conf = predecir(path)
    if conf >= UMBRAL_CONFIANZA:
        if not os.path.exists(DESTINO):
            os.makedirs(DESTINO)
        destino = os.path.join(DESTINO, f"{pred}.png")
        shutil.copy(path, destino)
        print(f"[✓] Autoetiquetado: {pred} (confianza: {conf:.2f})")
    else:
        print(f"[✗] Confianza baja: {pred} ({conf:.2f}), no se guarda")

if __name__ == "__main__":
    autoetiquetar()
