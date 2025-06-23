import torch
import torch.nn as nn
import torch.optim as optim
from preparar_datos import vectorizar_partida
import os

from config import SINERGIAS_FIJAS

# Recolectar todos los archivos .json generados
archivos = [f for f in os.listdir() if f.startswith("partida_") and f.endswith(".json")]

# Combinar datos de todas las partidas
ejemplos = []
for archivo in archivos:
    ejemplos += vectorizar_partida(archivo)

entradas = [torch.tensor(e[0], dtype=torch.float32) for e in ejemplos]
salidas = [torch.tensor(e[1], dtype=torch.long) for e in ejemplos]

X = torch.stack(entradas)
y = torch.zeros((len(salidas), 5), dtype=torch.float32)
for i, salida in enumerate(salidas):
    for idx in salida:
        if 0 <= idx < 5:
            y[i, idx] = 1

modelo = nn.Sequential(
    nn.Linear(9 + len(SINERGIAS_FIJAS), 32),
    nn.ReLU(),
    nn.Linear(32, 5),
    nn.Sigmoid()
)

criterio = nn.BCELoss()
optimizador = optim.Adam(modelo.parameters(), lr=0.01)

for epoca in range(300):
    salida_pred = modelo(X)
    perdida = criterio(salida_pred, y)
    optimizador.zero_grad()
    perdida.backward()
    optimizador.step()

    if epoca % 100 == 0:
        print(f"🧠 Época {epoca} - Pérdida: {perdida.item():.4f}")

torch.save(modelo.state_dict(), "modelo_compra.pth")
print("✅ Modelo mejorado guardado con datos de múltiples partidas.")
