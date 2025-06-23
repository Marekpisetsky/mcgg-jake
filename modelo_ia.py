import torch
import torch.nn as nn
from preparar_datos import heroes_id
from config import SINERGIAS_FIJAS
from collections import Counter
from sinergias import datos_heroes

# Red neuronal igual a la del entrenamiento
modelo = nn.Sequential(
    nn.Linear(6 + len(SINERGIAS_FIJAS), 32),
    nn.ReLU(),
    nn.Linear(32, 5),
    nn.Sigmoid()
)

# Cargar el modelo entrenado
import os

if os.path.exists("modelo_compra.pth"):
    modelo.load_state_dict(torch.load("modelo_compra.pth"))
else:
    print("⚠️ No se encontró modelo_compra.pth. Se usará un modelo sin entrenar.")

modelo.eval()

def decision_ia(estado):
    oro = estado["oro"]
    tienda = [heroes_id.get(h, 0) for h in estado["tienda"]]
    tienda += [0] * (5 - len(tienda))  # Rellenar si hay menos de 5

    # Extra features para IA
    ronda = estado.get("ronda", 1)
    costo_total = 2 * len(estado.get("banco", []))  # simulación
    tamaño_tienda = len(estado["tienda"])
    heroes_unicos = len(set(estado["tienda"]))
    repeticiones = len(estado["tienda"]) - heroes_unicos

    # Obtener sinergias actuales del banco
    banco = estado.get("banco", [])
    sinergias_actuales = []
    for nombre in banco:
        sinergias_actuales += datos_heroes.get(nombre, [])
    conteo_sinergias = dict(Counter(sinergias_actuales))

    sinergias_vector = [0] * len(SINERGIAS_FIJAS)
    for nombre in conteo_sinergias:
        if nombre in SINERGIAS_FIJAS:
            idx = SINERGIAS_FIJAS.index(nombre)
            sinergias_vector[idx] = 1

    entrada_vector = [
        oro,
        ronda,
        costo_total,
        tamaño_tienda,
        heroes_unicos,
        repeticiones
    ] + sinergias_vector

    entrada = torch.tensor(entrada_vector, dtype=torch.float32)
    salida = modelo(entrada)

    decisiones = []
    for i, valor in enumerate(salida):
        if i < len(estado["tienda"]) and valor.item() > 0.5 and oro >= 2:
            decisiones.append(f"Comprar {estado['tienda'][i]}")
            oro -= 2

    return decisiones

def decision_ia_con_modelo(estado, modelo):
    oro = estado["oro"]
    tienda = [heroes_id.get(h, 0) for h in estado["tienda"]]
    tienda += [0] * (5 - len(tienda))

    entrada = torch.tensor([oro] + tienda, dtype=torch.float32)
    salida = modelo(entrada)

    decisiones = []
    for i, valor in enumerate(salida):
        if valor.item() > 0.5 and oro >= 2:
            decisiones.append(f"Comprar {estado['tienda'][i]}")
            oro -= 2
    return decisiones
