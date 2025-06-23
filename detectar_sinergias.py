"""Detección de sinergias usando el detector de objetos."""

import cv2
import pyautogui
import json
import os

from detection import load_detector, detect

X_BASE = 5
Y_BASE = 180
ANCHO = 35
ALTO = 35
ESPACIADO_Y = 45
NUM_ICONOS = 19

_detector = None

def cargar_etiquetas(path="sinergias.json"):
    if not os.path.exists(path):
        return {str(i): f"sinergia_{i}" for i in range(NUM_ICONOS)}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def _ensure_detector():
    global _detector
    if _detector is None:
        _detector = load_detector("detector.pth")


def detectar_sinergias_activas():
    _ensure_detector()
    etiquetas = cargar_etiquetas()
    captura = pyautogui.screenshot()
    resultados = detect(_detector, captura, 0.4)
    activas = []
    for label, box, score in resultados:
        if label.startswith("sinergia") and score >= 0.5:
            activas.append(label)
    return activas
