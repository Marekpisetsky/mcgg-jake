"""Explora la interfaz de forma aleatoria mientras recopila capturas.

El script realiza taps en posiciones aleatorias y guarda imágenes en el dataset
usando ``autoentrenar_detector.guardar_captura`` si existe un modelo
``detector.pth``. Sirve para ampliar el conjunto de entrenamiento de forma
autónoma.
"""

import os
import random
import time
from pathlib import Path

import io_backend
from autoentrenar_detector import guardar_captura, DATASET_DIR, ANNOTATIONS_FILE
from detection import load_detector


def main() -> None:
    detector = None
    if Path("detector.pth").exists():
        detector = load_detector("detector.pth")
    print("[🧭] Exploración aleatoria iniciada")

    while True:
        x = random.randint(100, 1100)
        y = random.randint(100, 600)
        try:
            io_backend.tap(x, y)
            print(f"[TAP] ({x}, {y})")
        except io_backend.ADBError as exc:
            print(f"[ADB ERROR] {exc}")

        if detector is not None:
            guardar_captura(detector)
        else:
            img = io_backend.screenshot()
            if img is not None:
                DATASET_DIR.mkdir(parents=True, exist_ok=True)
                ANNOTATIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
                filename = f"{int(time.time() * 1000)}.png"
                img.save(DATASET_DIR / filename)
        time.sleep(0.5)


if __name__ == "__main__":
    main()
