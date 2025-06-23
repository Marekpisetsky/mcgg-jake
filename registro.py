import json

def guardar_partida(nombre_archivo, historial):
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        json.dump(historial, archivo, indent=4, ensure_ascii=False)
