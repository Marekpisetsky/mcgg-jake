import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
import os
from preparar_datos import vectorizar_partida
from config import SINERGIAS_FIJAS

# Buscar todos los archivos partida_XX.json reales
carpeta = os.path.dirname(os.path.abspath(__file__))
archivos = sorted([
    f for f in os.listdir(carpeta)
    if f.startswith("partida_") and f.endswith(".json") and f != "partida_simulada.json"
])

# Cargar y combinar ejemplos
ejemplos = []
for archivo in archivos:
    ruta = os.path.join(carpeta, archivo)
    ejemplos += vectorizar_partida(ruta)

# Tensores
X = torch.stack([torch.tensor(e[0], dtype=torch.float32) for e in ejemplos])
y = torch.zeros((len(ejemplos), 5), dtype=torch.float32)
for i, e in enumerate(ejemplos):
    for idx in e[1]:
        if 0 <= idx < 5:
            y[i, idx] = 1

# Modelo
modelo = nn.Sequential(
    nn.Linear(6 + len(SINERGIAS_FIJAS), 32),
    nn.ReLU(),
    nn.Linear(32, 5),
    nn.Sigmoid()
)

criterio = nn.BCELoss()
optimizador = optim.Adam(modelo.parameters(), lr=0.01)

# Entrenamiento
perdidas = []
for epoca in range(300):
    salida_pred = modelo(X)
    perdida = criterio(salida_pred, y)

    optimizador.zero_grad()
    perdida.backward()
    optimizador.step()
    
    perdidas.append(perdida.item())
    if epoca % 50 == 0:
        print(f"📘 Época {epoca} - Pérdida: {perdida.item():.4f}")

# Guardar modelo
torch.save(modelo.state_dict(), "modelo_compra.pth")
print("✅ Nuevo modelo entrenado guardado como modelo_compra.pth")

# Gráfica de pérdida
plt.plot(perdidas)
plt.xlabel("Época")
plt.ylabel("Pérdida")
plt.title("Pérdida durante el entrenamiento (múltiples partidas)")
plt.grid(True)
plt.tight_layout()
plt.savefig("grafica_entrenamiento_varios.png")
plt.show()
