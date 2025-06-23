# guardar_ejemplo_oro.py
import cv2
import os

ORIGEN = "frame_oro.png"
DESTINO = "oro_dataset"

def guardar_ejemplo(etiqueta):
    if not os.path.exists(DESTINO):
        os.makedirs(DESTINO)

    img = cv2.imread(ORIGEN)
    nombre_archivo = os.path.join(DESTINO, f"{etiqueta}.png")
    cv2.imwrite(nombre_archivo, img)
    print(f"[✓] Guardado como {nombre_archivo}")

if __name__ == "__main__":
    etiqueta = input("¿Qué número aparece en frame_oro.png? ")
    guardar_ejemplo(etiqueta)
