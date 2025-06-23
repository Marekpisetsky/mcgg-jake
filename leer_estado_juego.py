# leer_estado_juego.py

from leer_ronda_automatica import detectar_ronda as obtener_ronda
from leer_oro_automatico import detectar_oro
from detectar_sinergias import detectar_sinergias_activas

# El código original no contemplaba la lectura de la tienda ni el banco.
# Para evitar errores en módulos que esperan estas claves, se devolverán
# listas vacías por defecto.


def leer_estado_juego():
    """
    Devuelve el estado actual del juego.
    Incluye: ronda, sinergias activas, cantidad de oro.
    """
    estado = {}

    try:
        ronda = obtener_ronda()
        estado["ronda"] = ronda
    except Exception as e:
        estado["ronda"] = None
        print(f"[ERROR] No se pudo leer la ronda: {e}")

    try:
        sinergias = detectar_sinergias_activas()
        estado["sinergias"] = sinergias
    except Exception as e:
        estado["sinergias"] = []
        print(f"[ERROR] No se pudo leer las sinergias: {e}")

    try:
        oro = detectar_oro()
        estado["oro"] = oro
    except Exception as e:
        estado["oro"] = None
        print(f"[ERROR] No se pudo leer el oro: {e}")

    # Claves opcionales utilizadas por otros módulos.
    # Se devuelven listas vacías para evitar KeyError si aún no se ha
    # implementado la detección automática de la tienda o del banco.
    estado.setdefault("tienda", [])
    estado.setdefault("banco", [])

    return estado


# Prueba directa
if __name__ == "__main__":
    estado = leer_estado_juego()
    print("Estado actual del juego:", estado)
