import os
from simulador import simular_rondas
import subprocess

def borrar_partidas():
    for archivo in os.listdir():
        if archivo.startswith("partida_") and archivo.endswith(".json"):
            os.remove(archivo)

for ciclo in range(1, 11):  # Cambia a 1000 si quieres algo eterno
    print(f"\n🔁 CICLO DE APRENDIZAJE {ciclo}\n")

    # 1. Borrar partidas anteriores
    borrar_partidas()

    # 2. Generar nuevas partidas simuladas
    for i in range(1, 11):
        nombre_archivo = f"partida_{i:02}.json"
        simular_rondas(numero_rondas=5, archivo=nombre_archivo)

    # 3. Entrenar con todos los datos nuevos
    subprocess.run(["python", "entrenar_con_todo.py"])
