# config.py

# Lista fija y ordenada de todas las sinergias posibles en el simulador
SINERGIAS_FIJAS = [
    "Marksman", "Fighter", "Tank", "Lightborn", "Northern Vale",
    "Mage", "Elementalist", "Assassin", "Mecha", "Undead",
    "Wrestler", "Elf", "Dragon"
]

# Selección del modo de interacción con el juego.
# "desktop" utiliza pyautogui sobre una ventana (emulador/scrcpy).
# "mobile" emplea adb para capturas y toques en un dispositivo conectado.
IO_MODE = "desktop"
