import streamlit as st
from estado_juego import obtener_estado_inicial
from modelo_ia import decision_ia
import random

heroes_disponibles = [
    "Layla", "Zilong", "Tigreal", "Franco", "Eudora",
    "Saber", "Bane", "Freya", "Karina", "Akai"
]

def generar_tienda():
    return random.sample(heroes_disponibles, 5)

# Título
st.title("🎯 Simulación de Decisiones de la IA (mcgg-jake)")

# Estado inicial
estado = obtener_estado_inicial()
estado["tienda"] = generar_tienda()
oro_inicial = estado["oro"]

# Mostrar estado
st.subheader(f"💰 Oro: {estado['oro']}")
st.subheader(f"🛍️ Tienda:")
st.write(estado["tienda"])

# Botón de decisión
if st.button("🤖 Decidir con IA"):
    decisiones = decision_ia(estado)
    st.success("🧠 Decisiones tomadas:")
    for d in decisiones:
        st.write("👉", d)

    st.info("📝 Estado de la ronda actual:")
    st.json(estado)
else:
    st.warning("Haz clic en el botón para ver las decisiones de la IA.")
