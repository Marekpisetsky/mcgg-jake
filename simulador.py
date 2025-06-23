from estado_juego import obtener_estado_inicial
from sinergias import datos_heroes
from collections import Counter
from registro import guardar_partida
from preparar_datos import vector_entrada
import torch
import random
import json

def simular_rondas(modelo, numero_rondas=3, archivo="partida_simulada.json"):
    estado = obtener_estado_inicial()
    estado["banco"] = []
    historial = []

    racha = 0
    racha_tipo = None
    victorias = 0

    for ronda in range(1, numero_rondas + 1):
        estado["ronda"] = ronda
        print(f"\n🎯 RONDA {ronda}")
        print(f"Oro: {estado['oro']}")
        print(f"Tienda: {estado['tienda']}")

        # IA toma decisiones usando el modelo
        entrada = torch.tensor(vector_entrada(estado), dtype=torch.float32)
        salida = modelo(entrada)

        decisiones = []
        oro_disp = estado["oro"]

        for i, valor in enumerate(salida):
            if valor.item() > 0.5 and oro_disp >= 2:
                nombre = estado["tienda"][i]
                decisiones.append(f"Comprar {nombre}")
                oro_disp -= 2
                estado["banco"].append(nombre)

        print(*["👉 " + d for d in decisiones], sep="\n")

        # Aplicar costo
        estado["oro"] = max(0, estado["oro"] - (2 * len(decisiones)))

        # Simular resultado
        gana = random.random() > 0.5
        if gana:
            victorias += 1

        # Actualizar racha
        if gana:
            racha = racha + 1 if racha_tipo == "victoria" else 1
            racha_tipo = "victoria"
        else:
            racha = racha + 1 if racha_tipo == "derrota" else 1
            racha_tipo = "derrota"

        # Calcular oro extra
        oro_extra = 5
        if gana:
            oro_extra += 1
        if racha >= 2:
            oro_extra += min(3, racha)

        estado["oro"] += oro_extra

        # Calcular sinergias
        sinergias_actuales = []
        for nombre in estado["banco"]:
            sinergias_actuales += datos_heroes.get(nombre, [])

        conteo_sinergias = dict(Counter(sinergias_actuales))

        historial.append({
            "ronda": ronda,
            "oro_inicial": estado["oro"],
            "tienda": estado["tienda"],
            "acciones": decisiones,
            "gano": gana,
            "oro_ganado": oro_extra,
            "racha_actual": racha,
            "tipo_racha": racha_tipo,
            "sinergias": conteo_sinergias
        })

        # Nueva tienda
        todos_los_heroes = ["Layla", "Saber", "Franco", "Bane", "Freya", "Zilong", "Eudora", "Karina", "Akai"]
        estado["tienda"] = random.sample(todos_los_heroes, 5)

    guardar_partida(archivo, historial)
    return victorias, numero_rondas


# Si se ejecuta como script independiente
if __name__ == "__main__":
    import torch.nn as nn
    from config import SINERGIAS_FIJAS
    import os

    modelo = nn.Sequential(
        nn.Linear(10 + len(SINERGIAS_FIJAS), 32),
        nn.ReLU(),
        nn.Linear(32, 5),
        nn.Sigmoid()
    )

    # Cargar modelo si existe
    if os.path.exists("modelo_compra.pth"):
        modelo.load_state_dict(torch.load("modelo_compra.pth"))
        modelo.eval()

    total_victorias = 0
    total_partidas = 10

    for i in range(1, total_partidas + 1):
        archivo = f"partida_{i:02}.json"
        victorias, rondas = simular_rondas(modelo, numero_rondas=5, archivo=archivo)
        if victorias > 0:
            total_victorias += 1  # Cuenta la partida como victoria si ganó alguna ronda

    winrate = (total_victorias / total_partidas) * 100
    print(f"\n🏁 Winrate total: {winrate:.2f}%")

    # Guardar winrate
    with open("winrate.txt", "a") as f:
        f.write(f"{winrate:.2f}\n")
