import torch
from simulador import simular_rondas
from preparar_datos import heroes_id
from modelo_ia import modelo, decision_ia_con_modelo
from entrenar_modelo import entrenar_modelo
import os

# Ruta del modelo
modelo_path = "modelo_compra.pth"

# 1️⃣ Simular sin entrenamiento
print("\n🚫 Simulando partidas con IA sin entrenar...")
for i in range(5):
    simular_rondas(numero_rondas=5, archivo=f"sin_entrenar_{i}.json", modelo=modelo)

# 2️⃣ Entrenar modelo
print("\n🧠 Entrenando modelo...")
modelo_entrenado = entrenar_modelo()  # <- Esta función debes retornar el modelo al final de entrenar_modelo.py

# 3️⃣ Simular con modelo entrenado
print("\n✅ Simulando partidas con IA entrenada...")
for i in range(5):
    simular_rondas(numero_rondas=5, archivo=f"entrenado_{i}.json", modelo=modelo_entrenado)
