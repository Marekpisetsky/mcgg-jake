from PIL import Image
import torch
from torchvision import transforms
import logging

logging.basicConfig(level=logging.INFO)

# Cargar el modelo entrenado una vez
modelo = torch.load("modelo_oro.pt")
modelo.eval()

# Transformaciones de imagen
transform = transforms.Compose([
    transforms.Resize((64, 64)),
    transforms.ToTensor()
])

# Función de predicción
def predecir_oro(ruta_imagen):
    try:
        # Abrir imagen con PIL
        imagen = Image.open(ruta_imagen).convert("RGB")
        imagen = transform(imagen).unsqueeze(0)

        # Ejecutar el modelo
        with torch.no_grad():
            salida = modelo(imagen)

        prediccion = salida.item()
        return int(round(prediccion)), prediccion
    except Exception as e:
        logging.error("[✗] Error al predecir oro: %s", e)
        return -1, -1

# Ejemplo de uso
def main():
    oro, confianza = predecir_oro("frame_oro.png")
    if oro == -1:
        logging.error("[✗] Error al procesar la imagen.")
    else:
        logging.info("[✓] Oro detectado: %d (confianza: %.4f)", oro, confianza)

if __name__ == "__main__":
    main()
