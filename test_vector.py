# test_vector.py

from preparar_datos import vectorizar_partida

ejemplos = vectorizar_partida("partida_simulada.json")

for entrada, salida in ejemplos:
    print("🔢 Entrada:", entrada)
    print("🎯 Salida esperada:", salida)
    print()
