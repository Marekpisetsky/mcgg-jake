# aprendizaje_continuo.py
import os
import time
from oro_autoentrenar import entrenar

EJEMPLOS_ENTRENADOS = set()
TIEMPO_ESPERA = 5  # segundos

def contar_ejemplos():
    return set(f for f in os.listdir("oro_dataset") if f.endswith(".png"))

def main():
    print("[🚀] Iniciando aprendizaje continuo...")
    while True:
        os.system("python mcgg_jake_runner.py")

        nuevos = contar_ejemplos()
        diferencia = nuevos - EJEMPLOS_ENTRENADOS

        if len(diferencia) >= 10:
            print(f"[📚] Se detectaron {len(diferencia)} ejemplos nuevos. Reentrenando...")
            entrenar()
            EJEMPLOS_ENTRENADOS.update(nuevos)
        else:
            print(f"[⏳] Aún no hay suficientes nuevos ejemplos ({len(diferencia)}/10)")

        time.sleep(TIEMPO_ESPERA)

if __name__ == "__main__":
    os.makedirs("oro_dataset", exist_ok=True)
    EJEMPLOS_ENTRENADOS = contar_ejemplos()
    main()
