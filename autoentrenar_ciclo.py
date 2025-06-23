# autoentrenar_ciclo.py
import os
from oro_autoentrenar import entrenar

def contar_archivos(carpeta):
    return len([f for f in os.listdir(carpeta) if f.endswith(".png")])

if __name__ == "__main__":
    if contar_archivos("oro_dataset") >= 75:  # por ejemplo
        print("[•] Entrenando con ejemplos recolectados...")
        entrenar()
    else:
        print("[!] No hay suficientes ejemplos nuevos todavía.")
