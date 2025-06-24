import json
from collections import Counter

from sinergias import datos_heroes


# Create the mapping ``hero -> id`` dynamically using ``sinergias.py`` so that
# new heroes only require updating that file or the dataset.
heroes_id = {name: idx + 1 for idx, name in enumerate(sorted(datos_heroes.keys()))}

def vectorizar_partida(nombre_archivo):
    with open(nombre_archivo, encoding="utf-8") as archivo:
        datos = json.load(archivo)

    ejemplos = []

    for ronda in datos:
        oro = ronda["oro_inicial"]
        nivel = ronda.get("nivel", 0) or 0
        tienda = [heroes_id.get(h, 0) for h in ronda["tienda"]]
        tienda += [0] * (5 - len(tienda))  # relleno si hay menos de 5

        # Placeholder para niveles de estrellas (no disponible en datos)
        estrellas_vector = [0, 0, 0]

        # Extraer sinergias (rellenar con 0 si faltan)
        sinergias_vector = [0] * len(SINERGIAS_FIJAS)
        ronda_sinergias = ronda.get("sinergias", {})

        for i, nombre in enumerate(SINERGIAS_FIJAS):
            if nombre in ronda_sinergias:
                sinergias_vector[i] = ronda_sinergias[nombre]

        entrada = [oro, nivel] + tienda + estrellas_vector + sinergias_vector

        salida = []

        for accion in ronda["acciones"]:
            if accion.startswith("Comprar"):
                nombre = accion.replace("Comprar ", "").strip()
                idx = ronda["tienda"].index(nombre)
                salida.append(idx)  # la posición en tienda

        ejemplos.append((entrada, salida))

    return ejemplos

from config import SINERGIAS_FIJAS
from sinergias import datos_heroes


def vector_entrada(estado):
    oro = estado.get("oro", 0) or 0
    nivel = estado.get("nivel", 0) or 0
    tienda = [heroes_id.get(h, 0) for h in estado["tienda"]]
    tienda += [0] * (5 - len(tienda))  # asegurar que tenga 5 valores

    banco = estado.get("banco", [])

    # calcular niveles de estrellas
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

    # calcular sinergias del banco
    sinergias = []
    for nombre in banco:
        sinergias += datos_heroes.get(nombre, [])

    conteo = {k: 0 for k in SINERGIAS_FIJAS}
    for s in sinergias:
        if s in conteo:
            conteo[s] += 1

    vector_sinergias = list(conteo.values())
    return [oro, nivel] + tienda + vector_estrellas + vector_sinergias
