# aprendizaje_continuo.py
import os
import time
import subprocess
import logging
from oro_autoentrenar import entrenar

logging.basicConfig(level=logging.INFO)

EJEMPLOS_ENTRENADOS = set()
TIEMPO_ESPERA = 5  # segundos

def contar_ejemplos():
    return set(f for f in os.listdir("oro_dataset") if f.endswith(".png"))

def main():
    logging.info("[🚀] Iniciando aprendizaje continuo...")
    while True:
        try:
            subprocess.run(["python", "mcgg_jake_runner.py"], check=True)
        except subprocess.CalledProcessError as exc:
            logging.error("mcgg_jake_runner.py failed: %s", exc)
            continue

        nuevos = contar_ejemplos()
        diferencia = nuevos - EJEMPLOS_ENTRENADOS

        if len(diferencia) >= 10:
            logging.info(
                "[📚] Se detectaron %d ejemplos nuevos. Reentrenando...",
                len(diferencia),
            )
            entrenar()
            EJEMPLOS_ENTRENADOS.update(nuevos)
        else:
            logging.info(
                "[⏳] Aún no hay suficientes nuevos ejemplos (%d/10)",
                len(diferencia),
            )

        time.sleep(TIEMPO_ESPERA)

if __name__ == "__main__":
    os.makedirs("oro_dataset", exist_ok=True)
    EJEMPLOS_ENTRENADOS = contar_ejemplos()
    main()
