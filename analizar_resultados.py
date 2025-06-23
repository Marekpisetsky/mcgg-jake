import json
import os
import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict

# Ruta actual segura
carpeta = os.path.dirname(os.path.abspath(__file__))
archivos = sorted([
    f for f in os.listdir(carpeta)
    if f.startswith("partida_") and f.endswith(".json")
])

estadisticas = []

for archivo in archivos:
    ruta = os.path.join(carpeta, archivo)
    with open(ruta, "r", encoding="utf-8") as f:
        datos = json.load(f)

    if not datos:
        continue

    victorias = sum(1 for ronda in datos if ronda.get("gano"))
    total = len(datos)
    oro_final = datos[-1].get("oro_inicial", 0)
    sinergias = datos[-1].get("sinergias", {})
    
    estadisticas.append({
        "archivo": archivo,
        "rondas": total,
        "victorias": victorias,
        "winrate (%)": round(100 * victorias / total, 1),
        "oro final": oro_final,
        "sinergias": sinergias
    })

# Crear DataFrame
df = pd.DataFrame(estadisticas)

# Mostrar resumen
print("\n📊 RESUMEN DE PARTIDAS")
print(df[["archivo", "rondas", "victorias", "winrate (%)", "oro final"]])

# Graficar
plt.figure(figsize=(10, 5))
plt.plot(df["archivo"], df["winrate (%)"], marker="o", label="Tasa de victoria")
plt.title("Winrate por partida simulada")
plt.ylabel("Winrate (%)")
plt.xlabel("Partida")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()
