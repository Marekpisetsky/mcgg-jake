"""Orquesta el entrenamiento completamente autonomo.

Se lanza un hilo para el autoentrenamiento del detector mientras el bucle de
``main_loop`` juega partidas y actualiza el agente DQN.
"""

from threading import Thread
import autoentrenar_detector
import main_loop


def _run_detector():
    autoentrenar_detector.main()


def main() -> None:
    detector_thread = Thread(target=_run_detector, daemon=True)
    detector_thread.start()
    main_loop.train_loop()


if __name__ == "__main__":
    main()
