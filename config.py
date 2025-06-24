# config.py

# Lista fija y ordenada de todas las sinergias posibles en el simulador
SINERGIAS_FIJAS = [
    "Altar del Dragón",
    "Apoyo",
    "Astrónomo",
    "Defensor",
    "Eruditio",
    "Espadachin",
    "Exorcista",
    "Hadanacido",
    "Intrépido",
    "Invocador",
    "Juraperdición",
    "Maestros de Armas",
    "Mago",
    "Poder Astral",
    "Portador del Amanecer",
    "Señor de Ascuas",
    "Tejedor de Sombras",
    "Tirador",
    "Valle del Norte",
]

# Modo de interacción para entrada/salida.
# "desktop" usa pyautogui local, "mobile" utiliza ADB.
IO_MODE = "mobile"

# Coordenadas (x, y) de cada slot de héroe en la tienda. Ajustar según la
# resolución del dispositivo usado.
SHOP_SLOT_COORDS = [
    (350, 270),  # Slot 0 - izquierda
    (510, 270),  # Slot 1
    (680, 270),  # Slot 2
    (860, 270),  # Slot 3
    (1015, 270),  # Slot 4 - derecha
]

# Región (x, y, ancho, alto) donde aparece el texto de victoria/derrota.
FIN_PARTIDA_REGION = (250, 100, 300, 80)
