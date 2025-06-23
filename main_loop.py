import time
import json
import argparse

import pyautogui

from leer_estado_juego import leer_estado_juego
from modelo_ia import decision_ia
from agent import Agent


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
    historial = []
    ronda_actual = 0
    # Agente de aprendizaje por refuerzo
    agent = Agent(state_size=3, action_size=2)

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

        agent.update_policy((estado_vector, accion_idx, recompensa, siguiente_vector, False))

        registro_ronda = {
            "ronda": estado_resultante.get("ronda"),
            "oro": estado_resultante.get("oro"),
            "sinergias": estado_resultante.get("sinergias", []),
            "acciones": acciones,
            "recompensa": recompensa,
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
