import time
import json
import argparse

import os
import pyautogui

from leer_estado_juego import leer_estado_juego
from modelo_ia import decision_ia
from rl.dqn import DQNAgent


def migrar_historial(historial):
    """Convierte el formato antiguo de historial al nuevo basado en transiciones."""
    if not historial:
        return []
    if isinstance(historial[0], dict) and "s" in historial[0]:
        return historial

    nuevo = []
    for i, ronda in enumerate(historial):
        s_vec = [
            ronda.get("oro", 0) or 0,
            ronda.get("ronda", 0) or 0,
            len(ronda.get("sinergias", [])),
        ]
        if i < len(historial) - 1:
            nxt = historial[i + 1]
            s_next = [
                nxt.get("oro", 0) or 0,
                nxt.get("ronda", 0) or 0,
                len(nxt.get("sinergias", [])),
            ]
            done = False
        else:
            s_next = s_vec
            done = True

        nuevo.append(
            {
                "s": s_vec,
                "a": 1 if ronda.get("acciones") else 0,
                "r": ronda.get("recompensa", 0),
                "s_next": s_next,
                "done": done,
                "acciones": ronda.get("acciones", []),
            }
        )
    return nuevo


def ejecutar_accion(accion):
    """Realiza un toque en pantalla usando pyautogui o adb.

    La accion puede ser una tupla (x, y) o un diccionario con claves "x" y "y".
    Otros formatos se ignoran mostrando un mensaje informativo.
    """
    x = y = None

    if isinstance(accion, (list, tuple)) and len(accion) >= 2:
        x, y = accion[0], accion[1]
    elif isinstance(accion, dict) and "x" in accion and "y" in accion:
        x, y = accion["x"], accion["y"]
    elif isinstance(accion, str) and accion.startswith("tap "):
        try:
            _, xs, ys = accion.split()
            x, y = int(xs), int(ys)
        except ValueError:
            pass

    if x is not None and y is not None:
        pyautogui.click(x, y)
        print(f"[✓] Click en ({x}, {y})")
    else:
        print(f"[!] Formato de acción no reconocido: {accion}")


def main(numero_rondas=None, archivo="partida_ia.json"):
    """Ejecuta el ciclo principal de mcgg-jake.

    Si ``numero_rondas`` es ``None`` el ciclo se repite indefinidamente.
    Cada iteración lee el estado actual, calcula las acciones con la IA,
    ejecuta dichas acciones y guarda el resultado acumulado en ``archivo``.
    """
    if os.path.exists(archivo):
        try:
            with open(archivo, encoding="utf-8") as f:
                historial = json.load(f)
        except Exception:
            historial = []
        historial = migrar_historial(historial)
    else:
        historial = []
    ronda_actual = len(historial)
    agent = DQNAgent(state_size=3, action_size=2)
    for trans in historial:
        if all(k in trans for k in ("s", "a", "r", "s_next", "done")):
            agent.remember((trans["s"], trans["a"], trans["r"], trans["s_next"], trans["done"]))

    while True:
        estado = leer_estado_juego()

        estado_vector = [
            estado.get("oro", 0) or 0,
            estado.get("ronda", 0) or 0,
            len(estado.get("sinergias", [])),
        ]

        accion_idx = agent.select_action(estado_vector)
        acciones = decision_ia(estado) if accion_idx == 1 else []

        for accion in acciones:
            ejecutar_accion(accion)
            time.sleep(0.5)

        estado_resultante = leer_estado_juego()
        recompensa = (estado_resultante.get("oro", 0) or 0) - (estado.get("oro", 0) or 0)

        siguiente_vector = [
            estado_resultante.get("oro", 0) or 0,
            estado_resultante.get("ronda", 0) or 0,
            len(estado_resultante.get("sinergias", [])),
        ]

        done = numero_rondas is not None and ronda_actual + 1 >= numero_rondas
        agent.remember((estado_vector, accion_idx, recompensa, siguiente_vector, done))
        agent.train_step()

        registro_ronda = {
            "s": estado_vector,
            "a": accion_idx,
            "r": recompensa,
            "s_next": siguiente_vector,
            "done": done,
            "acciones": acciones,
        }
        historial.append(registro_ronda)

        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(historial, f, indent=2, ensure_ascii=False)

        ronda_actual += 1
        if numero_rondas is not None and ronda_actual >= numero_rondas:
            break

        time.sleep(2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bucle principal de mcgg-jake")
    parser.add_argument("-n", "--rondas", type=int,
                        help="Número de rondas a ejecutar (infinito si se omite)")
    parser.add_argument("-o", "--output", default="partida_ia.json",
                        help="Archivo JSON donde guardar el historial")

    args = parser.parse_args()
    main(args.rondas, args.output)
