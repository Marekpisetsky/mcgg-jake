import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
import os
from pathlib import Path
from preparar_datos import vectorizar_partida
from config import SINERGIAS_FIJAS

def entrenar_modelo():
    # Datos
    archivo_base = "partida_simulada.json"
    if not os.path.exists(archivo_base):
        print(f"⚠️ No se encontró {archivo_base}. No se entrenará en este ciclo.")
        from modelo_ia import modelo  # importamos modelo sin entrenar
        return modelo

    ejemplos = vectorizar_partida(archivo_base)

    # Convertimos a tensores
    entradas = [torch.tensor(e[0], dtype=torch.float32) for e in ejemplos]
    salidas = [torch.tensor(e[1], dtype=torch.long) for e in ejemplos]

    # Dataset
    X = torch.stack(entradas)
    y = torch.zeros((len(salidas), 5), dtype=torch.float32)
    for i, salida in enumerate(salidas):
        for idx in salida:
            if 0 <= idx < 5:
                y[i, idx] = 1

    # Red neuronal
    modelo = nn.Sequential(
        nn.Linear(10 + len(SINERGIAS_FIJAS), 32),
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
            print(f"🧠 Época {epoca} - Pérdida: {perdida.item():.4f}")

    # Guardar modelo
    torch.save(modelo.state_dict(), "modelo_compra.pth")
    print("✅ Modelo entrenado y guardado como modelo_compra.pth")

    # Guardar gráfica de pérdida sin mostrar
    Path("graficas").mkdir(exist_ok=True)
    plt.plot(perdidas)
    plt.xlabel("Época")
    plt.ylabel("Pérdida")
    plt.title("Pérdida durante el entrenamiento")
    plt.grid(True)
    plt.savefig("graficas/perdida_entrenamiento.png")
    plt.close()
    print("📊 Gráfica guardada como graficas/perdida_entrenamiento.png")

    return modelo
