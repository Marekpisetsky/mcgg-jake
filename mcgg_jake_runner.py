# mcgg_jake_runner.py
import os
import cv2
import torch
import torch.nn as nn
from torchvision import transforms
from captura_pantalla import capturar_pantalla

# Definir el mismo modelo que entrenaste
class OroCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.red = nn.Sequential(
            nn.Conv2d(1, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(16, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Flatten(),
            nn.Linear(32 * 16 * 16, 128), nn.ReLU(),
            nn.Linear(128, 1000)
        )

    def forward(self, x):
        return self.red(x)

# Transformación igual a la usada en entrenamiento
transform = transforms.Compose([
    transforms.Grayscale(),
    transforms.Resize((64, 64)),
    transforms.ToTensor()
])

def predecir_oro(path="frame_oro.png"):
    imagen = cv2.imread(path)
    imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
    imagen = transform(imagen).unsqueeze(0)

    modelo = OroCNN()
    modelo.load_state_dict(torch.load("modelo_oro.pth"))
    modelo.eval()

    with torch.no_grad():
        salida = modelo(imagen)
        probs = torch.softmax(salida, dim=1)
        confianza, prediccion = torch.max(probs, dim=1)
        return prediccion.item(), confianza.item()

def main():
    print("[•] Capturando pantalla...")
    capturar_pantalla()

    print("[•] Detectando oro con IA...")
    oro, confianza = predecir_oro("frame_oro.png")
    print(f"[✓] Oro detectado: {oro} (confianza: {confianza:.2f})")

    # Guardar automáticamente como ejemplo si es confiable
    if confianza >= 0.98:
        nombre = f"oro_dataset/{oro}.png"
        os.makedirs("oro_dataset", exist_ok=True)
        cv2.imwrite(nombre, cv2.imread("frame_oro.png"))
        print(f"[↑] Añadido a entrenamiento: {nombre}")
    else:
        print("[!] Confianza baja, no se guardó para entrenamiento.")

if __name__ == "__main__":
    main()
