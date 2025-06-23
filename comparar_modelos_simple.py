import os
import json
import matplotlib.pyplot as plt

def cargar_winrates(prefix):
    winrates = []
    for i in range(5):
        archivo = f"{prefix}_{i}.json"
        if not os.path.exists(archivo):
            continue
        with open(archivo, encoding="utf-8") as f:
            datos = json.load(f)
        victorias = sum(1 for ronda in datos if ronda.get("gano"))
        total = len(datos)
        winrate = 100 * victorias / total if total else 0
        winrates.append(winrate)
    return winrates

# Cargar winrates
sin_entrenar = cargar_winrates("sin_entrenar")
entrenado = cargar_winrates("entrenado")

# Gráfica
plt.figure(figsize=(8, 5))
plt.plot(range(1, 6), sin_entrenar, marker='o', label="Sin entrenar")
plt.plot(range(1, 6), entrenado, marker='o', label="Entrenado")
plt.xticks(range(1, 6), [f"Partida {i}" for i in range(1, 6)])
plt.ylabel("Winrate (%)")
plt.title("Comparación de desempeño IA (antes vs después del entrenamiento)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
