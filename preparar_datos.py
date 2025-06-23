import json
from collections import Counter


# Asignar un número a cada héroe
heroes_id = {
    "Layla": 1, "Zilong": 2, "Tigreal": 3, "Franco": 4, "Eudora": 5,
    "Saber": 6, "Bane": 7, "Freya": 8, "Karina": 9, "Akai": 10
}

def vectorizar_partida(nombre_archivo):
    with open(nombre_archivo, encoding="utf-8") as archivo:
        datos = json.load(archivo)

    ejemplos = []

    for ronda in datos:
        oro = ronda["oro_inicial"]
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

        entrada = [oro] + tienda + estrellas_vector + sinergias_vector

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
    oro = estado["oro"]
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
    return [oro] + tienda + vector_estrellas + vector_sinergias
