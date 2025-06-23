import torch
import torch.nn as nn
from preparar_datos import heroes_id
from config import SINERGIAS_FIJAS
from collections import Counter
from sinergias import datos_heroes

# Red neuronal igual a la del entrenamiento
modelo = nn.Sequential(
    nn.Linear(9 + len(SINERGIAS_FIJAS), 32),
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
    # Usar 0 si el oro no está disponible o es None
    oro = estado.get("oro", 0) or 0
    tienda = [heroes_id.get(h, 0) for h in estado["tienda"]]
    tienda += [0] * (5 - len(tienda))  # Rellenar si hay menos de 5

    banco = estado.get("banco", [])

    # Niveles de estrellas del banco
    conteo_heroes = Counter(banco)
    estrella1 = estrella2 = estrella3 = 0
    for cantidad in conteo_heroes.values():
        if cantidad >= 9:
            estrella3 += 1
        elif cantidad >= 3:
            estrella2 += 1
        else:
            estrella1 += 1
    vector_estrellas = [estrella1, estrella2, estrella3]

    # Obtener sinergias actuales del banco
    sinergias_actuales = []
    for nombre in banco:
        sinergias_actuales += datos_heroes.get(nombre, [])
    conteo_sinergias = Counter(sinergias_actuales)

    sinergias_vector = [conteo_sinergias.get(s, 0) for s in SINERGIAS_FIJAS]

    entrada_vector = [
        oro
    ] + tienda + vector_estrellas + sinergias_vector

    entrada = torch.tensor(entrada_vector, dtype=torch.float32)
    salida = modelo(entrada)

    decisiones = []
    for i, valor in enumerate(salida):
        if i < len(estado["tienda"]) and valor.item() > 0.5 and oro >= 2:
            decisiones.append(f"Comprar {estado['tienda'][i]}")
            oro -= 2

    return decisiones

def decision_ia_con_modelo(estado, modelo):
    # Usar 0 si el oro no está disponible o es None
    oro = estado.get("oro", 0) or 0
    tienda = [heroes_id.get(h, 0) for h in estado["tienda"]]
    tienda += [0] * (5 - len(tienda))

    banco = estado.get("banco", [])

    conteo_heroes = Counter(banco)
    estrella1 = estrella2 = estrella3 = 0
    for cantidad in conteo_heroes.values():
        if cantidad >= 9:
            estrella3 += 1
        elif cantidad >= 3:
            estrella2 += 1
        else:
            estrella1 += 1
    vector_estrellas = [estrella1, estrella2, estrella3]

    sinergias = []
    for nombre in banco:
        sinergias += datos_heroes.get(nombre, [])
    conteo_sin = Counter(sinergias)
    vector_sinergias = [conteo_sin.get(s, 0) for s in SINERGIAS_FIJAS]

    entrada = torch.tensor([oro] + tienda + vector_estrellas + vector_sinergias,
                           dtype=torch.float32)
    salida = modelo(entrada)

    decisiones = []
    for i, valor in enumerate(salida):
        if valor.item() > 0.5 and oro >= 2:
            decisiones.append(f"Comprar {estado['tienda'][i]}")
            oro -= 2
    return decisiones
