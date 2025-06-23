import os
import time
import json
from pathlib import Path

from detection import load_detector, detect, train_detector, LABELS
import io_backend

DATASET_DIR = Path("dataset/images")
ANNOTATIONS_FILE = Path("dataset/annotations.json")
TRAIN_INTERVAL = 60 * 30  # 30 minutos

LABEL_TO_ID = {v: k for k, v in LABELS.items()}


def guardar_captura(detector):
    """Captura una imagen, la etiqueta con el detector y la guarda."""
    img = io_backend.screenshot()
    if img is None:
        return False

    DATASET_DIR.mkdir(parents=True, exist_ok=True)
    ANNOTATIONS_FILE.parent.mkdir(parents=True, exist_ok=True)

    filename = f"{int(time.time() * 1000)}.png"
    img_path = DATASET_DIR / filename
    img.save(img_path)

    results = detect(detector, img, 0.5)
    sample = {
        "file": filename,
        "boxes": [box for _, box, _ in results],
        "labels": [LABEL_TO_ID[label] for label, _, _ in results],
    }

    if ANNOTATIONS_FILE.exists():
        with open(ANNOTATIONS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    data.append(sample)
    with open(ANNOTATIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return True


def main():
    print("[🌀] Autoentrenamiento del detector iniciado")
    detector = load_detector("detector.pth") if Path("detector.pth").exists() else None
    last_train = time.time()

    while True:
        if detector is not None:
            guardar_captura(detector)
        else:
            # Sin modelo entrenado no se pueden etiquetar ejemplos
            img = io_backend.screenshot()
            if img is not None:
                DATASET_DIR.mkdir(parents=True, exist_ok=True)
                filename = f"{int(time.time() * 1000)}.png"
                img.save(DATASET_DIR / filename)
        time.sleep(1)

        if time.time() - last_train >= TRAIN_INTERVAL:
            print("[📚] Entrenando detector con nuevas capturas...")
            train_detector(str(DATASET_DIR), str(ANNOTATIONS_FILE), "detector.pth")
            detector = load_detector("detector.pth")
            last_train = time.time()
            print("[✓] Detector actualizado")


if __name__ == "__main__":
    main()
