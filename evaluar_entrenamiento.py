import torch
from simulador import simular_rondas
from entrenar_modelo import entrenar_modelo
from modelo_ia import modelo as modelo_inicial
import matplotlib.pyplot as plt
import os

# ───────────────────────────────
# ⚙️ CONFIGURACIÓN
NUM_PARTIDAS = 10
RONDAS_POR_PARTIDA = 5
CARPETA_DATOS = "resultados_eval"

os.makedirs(CARPETA_DATOS, exist_ok=True)

# ───────────────────────────────
# 1️⃣ SIMULAR SIN ENTRENAR
print("🚫 Simulando sin entrenar...")
sin_entrenar_winrates = []

for i in range(NUM_PARTIDAS):
    archivo = f"{CARPETA_DATOS}/sin_entrenar_{i}.json"
    simular_rondas(modelo_inicial, numero_rondas=RONDAS_POR_PARTIDA, archivo=archivo)
    with open(archivo, "r") as f:
        data = f.read().count('"gano": true')
        winrate = data / RONDAS_POR_PARTIDA * 100
        sin_entrenar_winrates.append(winrate)

# ───────────────────────────────
# 2️⃣ ENTRENAR MODELO
print("🧠 Entrenando modelo...")
modelo_entrenado = entrenar_modelo()

# ───────────────────────────────
# 3️⃣ SIMULAR CON MODELO ENTRENADO
print("✅ Simulando con modelo entrenado...")
entrenado_winrates = []

for i in range(NUM_PARTIDAS):
    archivo = f"{CARPETA_DATOS}/entrenado_{i}.json"
    simular_rondas(modelo_entrenado, numero_rondas=RONDAS_POR_PARTIDA, archivo=archivo)
    with open(archivo, "r") as f:
        data = f.read().count('"gano": true')
        winrate = data / RONDAS_POR_PARTIDA * 100
        entrenado_winrates.append(winrate)

# ───────────────────────────────
# 📊 GRAFICAR COMPARACIÓN
plt.figure()
plt.plot(range(1, NUM_PARTIDAS+1), sin_entrenar_winrates, marker='o', label="Sin entrenar")
plt.plot(range(1, NUM_PARTIDAS+1), entrenado_winrates, marker='o', label="Entrenado")
plt.xlabel("Partida")
plt.ylabel("Winrate (%)")
plt.title("Evaluación del entrenamiento de IA")
plt.legend()
plt.grid(True)
plt.xticks(range(1, NUM_PARTIDAS+1))
plt.tight_layout()
plt.show()
