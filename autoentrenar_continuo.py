import torch
import os
import json
import time
from entrenar_modelo import entrenar_modelo
from simulador import simular_rondas
from pathlib import Path
from shutil import copyfile
from generar_reporte import generar_reporte

ARCHIVO_DATOS = "partida_simulada.json"
BACKUP_DIR = "backups"
PARTIDAS_POR_CICLO = 10
MAX_PARTIDAS_GLOBALES = 1000
MAX_BACKUPS = 5

# Crear carpeta de backups si no existe
os.makedirs(BACKUP_DIR, exist_ok=True)

# Borrar winrate.txt antes de empezar
with open("winrate.txt", "w") as f:
    pass

ciclo = 1

while True:
    print(f"\n🔁 Ciclo {ciclo}")

    # Entrenar con los datos actuales
    if os.path.exists(ARCHIVO_DATOS):
        modelo_actual = entrenar_modelo()
    else:
        print("⚠️ No se encontró 'partida_simulada.json'. Usando modelo sin entrenar.")
        from modelo_ia import modelo as modelo_actual

    # Simular nuevas partidas
    nuevos_archivos = []
    for i in range(PARTIDAS_POR_CICLO):
        nombre_archivo = f"partida_temp_{ciclo}_{i}.json"
        simular_rondas(modelo=modelo_actual, archivo=nombre_archivo, numero_rondas=5)
        nuevos_archivos.append(nombre_archivo)

    # Calcular winrate
    ganadas, total = 0, 0
    for archivo in nuevos_archivos:
        with open(archivo, encoding="utf-8") as f:
            partidas = json.load(f)
            ganadas += sum(1 for p in partidas if p.get("gano"))
            total += len(partidas)

    winrate = (ganadas / total) * 100 if total > 0 else 0.0
    print(f"📈 Winrate ciclo {ciclo}: {winrate:.1f}%")

    with open("winrate.txt", "a", encoding="utf-8") as f:
        f.write(f"{winrate:.2f}\n")

    with open("winrate_por_ciclo.txt", "a", encoding="utf-8") as f:
        f.write(f"{ciclo},{winrate:.2f}\n")

    # Combinar y conservar solo las últimas 1000 rondas
    partidas = []
    for archivo in nuevos_archivos:
        with open(archivo, encoding="utf-8") as f:
            partidas.extend(json.load(f))
        os.remove(archivo)

    if os.path.exists(ARCHIVO_DATOS):
        with open(ARCHIVO_DATOS, encoding="utf-8") as f:
            partidas_anteriores = json.load(f)
        partidas = partidas_anteriores + partidas

    if len(partidas) > MAX_PARTIDAS_GLOBALES:
        partidas = partidas[-MAX_PARTIDAS_GLOBALES:]  # solo las últimas 1000

    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
        json.dump(partidas, f, indent=2, ensure_ascii=False)

    # Guardar backup del archivo de datos
    backup_file = f"{BACKUP_DIR}/backup_ciclo_{ciclo:04}.json"
    copyfile(ARCHIVO_DATOS, backup_file)

    # Limitar backups a los últimos 5
    backups = sorted(Path(BACKUP_DIR).glob("backup_ciclo_*.json"))
    while len(backups) > MAX_BACKUPS:
        os.remove(backups[0])
        backups.pop(0)

    generar_reporte()
    ciclo += 1
    time.sleep(1)  # espera 1 segundo entre ciclos para evitar sobrecarga
