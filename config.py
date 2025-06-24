# config.py

# Lista fija y ordenada de todas las sinergias posibles en el simulador
SINERGIAS_FIJAS = [
    "Marksman", "Fighter", "Tank", "Lightborn", "Northern Vale",
    "Mage", "Elementalist", "Assassin", "Mecha", "Undead",
    "Wrestler", "Elf", "Dragon"
]

# Modo de interacción para entrada/salida.
# "desktop" usa pyautogui local, "mobile" utiliza ADB.
IO_MODE = "desktop"

# Coordenadas (x, y) de cada slot de héroe en la tienda. Ajustar según la
# resolución del dispositivo usado.
SHOP_SLOT_COORDS = [
    (80, 290),   # Slot 0 - izquierda
    (240, 290),  # Slot 1
    (400, 290),  # Slot 2
    (560, 290),  # Slot 3
    (720, 290),  # Slot 4 - derecha
]

# Región (x, y, ancho, alto) donde aparece el texto de victoria/derrota.
FIN_PARTIDA_REGION = (250, 100, 300, 80)
