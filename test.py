from estado_juego import obtener_estado_inicial
from motor_decisiones import decidir_compra

estado = obtener_estado_inicial()
decisiones = decidir_compra(estado)

print("Decisiones tomadas:")
for d in decisiones:
    print("-", d)
