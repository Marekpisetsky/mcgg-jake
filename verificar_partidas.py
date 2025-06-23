import json

with open("partida_simulada.json", encoding="utf-8") as f:
    datos = json.load(f)

ganadas = [p for p in datos if p.get("ganada") is True]
perdidas = [p for p in datos if p.get("ganada") is False]

print(f"Total de partidas: {len(datos)}")
print(f"Ganadas: {len(ganadas)}")
print(f"Perdidas: {len(perdidas)}")
print(f"Porcentaje de victoria: {(len(ganadas)/len(datos))*100:.2f}%")
