import torch
import os
import json
from entrenar_modelo import entrenar_modelo
from simulador import simular_rondas
from pathlib import Path

# Borrar archivos de winrate anteriores
with open("winrate.txt", "w") as f:
    pass  # Esto borra el contenido anterior

with open("winrate_por_ciclo.txt", "w") as f:
    pass  # Esto borra también el archivo que se usa para graficar

CICLOS = 5
PARTIDAS_POR_CICLO = 10
ARCHIVO_DATOS = "partida_simulada.json"

def combinar_datos():
    datos = []
    for archivo in Path(".").glob("entrenado_*.json"):
        with open(archivo, "r", encoding="utf-8") as f:
            datos.extend(json.load(f))
    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)

for ciclo in range(1, CICLOS + 1):
    print(f"\n🔁 Ciclo {ciclo}/{CICLOS}")

    # Entrenar modelo con los datos actuales (si existen)
    if os.path.exists(ARCHIVO_DATOS):
        modelo_actual = entrenar_modelo()
    else:
        print("⚠️ No se encontró 'partida_simulada.json'. Usando modelo sin entrenar.")
        from modelo_ia import modelo as modelo_actual  # modelo base no entrenado

    # Simular nuevas partidas
    nuevos_archivos = []
    for i in range(PARTIDAS_POR_CICLO):
        nombre_archivo = f"partida_temp_{ciclo}_{i}.json"
        simular_rondas(modelo=modelo_actual, archivo=nombre_archivo, numero_rondas=5)
        nuevos_archivos.append(nombre_archivo)

    # 📈 Calcular winrate del ciclo
    ganadas = 0
    total = 0
    for archivo in nuevos_archivos:
        with open(archivo, encoding="utf-8") as f:
            partidas = json.load(f)
            ganadas += sum(1 for p in partidas if p.get("gano"))
            total += len(partidas)

    winrate = (ganadas / total) * 100 if total > 0 else 0.0
    print(f"\n📈 Winrate del ciclo {ciclo}: {winrate:.1f}%")

    # Guardar en archivo histórico para graficar
    with open("winrate_por_ciclo.txt", "a", encoding="utf-8") as f:
        f.write(f"{ciclo},{winrate:.2f}\n")

    # Combinar todos los archivos temporales en uno
    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as salida:
        partidas = []
        for archivo in nuevos_archivos:
            with open(archivo, encoding="utf-8") as f:
                partidas += json.load(f)
            os.remove(archivo)  # limpiar archivos temporales
        json.dump(partidas, salida, indent=2, ensure_ascii=False)
