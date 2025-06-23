import matplotlib.pyplot as plt
import os

os.makedirs("graficas", exist_ok=True)
# Leer archivo de winrate por ciclo
with open("winrate_por_ciclo.txt", encoding="utf-8") as f:
    lineas = f.readlines()

ciclos = [int(l.strip().split(",")[0]) for l in lineas]
winrates = [float(l.strip().split(",")[1]) for l in lineas]

plt.plot(ciclos, winrates, marker="o")
plt.title("Evolución del winrate por ciclo")
plt.xlabel("Ciclo")
plt.ylabel("Winrate (%)")
plt.grid(True)

# 🔽 Reemplaza esto:
# plt.show()

# ✅ Por esto:
plt.savefig("graficas/winrate.png")
plt.close()
