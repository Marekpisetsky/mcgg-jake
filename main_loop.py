"""Main training loop using the DQN agent."""

import os
import time

import torch

import io_backend
from fin_partida import detectar_fin_partida
from leer_estado_juego import leer_estado_juego
from preparar_datos import vector_entrada
from rl.dqn import DQNAgent
import tienda_utils
from config import SINERGIAS_FIJAS


MODEL_PATH = "dqn_model.pth"

# Approximate screen coordinates (x, y) for each hero slot in the shop.
# These values are calibrated for an 800x360 resolution screenshot and can
# be adjusted if a different resolution is used.
SHOP_SLOT_COORDS = [
    (80, 290),   # Slot 0 - leftmost hero
    (240, 290),  # Slot 1
    (400, 290),  # Slot 2
    (560, 290),  # Slot 3
    (720, 290),  # Slot 4 - rightmost hero
]


def _ejecutar_accion(indice: int) -> None:
    """Tap on the corresponding hero slot in the shop."""

    if indice < 0 or indice >= len(SHOP_SLOT_COORDS):
        print(f"[ACTION] Índice de slot inválido: {indice}")
        return

    if not tienda_utils.tienda_presente():
        print("[ACTION] Tienda no detectada, no se ejecutó tap")
        return

    x, y = SHOP_SLOT_COORDS[indice]
    try:
        io_backend.tap(x, y)
        print(f"[ACTION] Tap en slot {indice} -> ({x}, {y})")
    except io_backend.ADBError as exc:
        print(f"[ADB ERROR] {exc}")


def _calcular_recompensa(prev_state: dict, next_state: dict) -> float:
    """Calculate reward considering gold, victories and synergies."""

    oro_prev = prev_state.get("oro", 0) or 0
    oro_next = next_state.get("oro", 0) or 0
    reward = float(oro_next - oro_prev)

    # Victory / defeat detection
    resultado = next_state.get("gano")
    if resultado is True:
        reward += 10.0
    elif resultado is False:
        reward -= 10.0

    # Synergy progress
    prev_sin = set(prev_state.get("sinergias", []))
    next_sin = set(next_state.get("sinergias", []))
    nuevas = next_sin - prev_sin
    for sinergia in nuevas:
        if sinergia in SINERGIAS_FIJAS:
            reward += 1.0

    return reward


def _reiniciar_partida() -> None:
    """Navigate the end-game menus and start a new match.

    Sends several key presses/taps until the shop is detected again. The
    coordinates are approximate and may require calibration for the target
    device.
    """

    print("[INFO] Reiniciando partida...")

    # Cerrar la pantalla de resultados
    for _ in range(3):
        try:
            io_backend.press("enter")
            time.sleep(1.0)
        except io_backend.ADBError as exc:
            print(f"[ADB ERROR] {exc}")
            break

    # Intentar iniciar la siguiente partida
    for _ in range(5):
        try:
            io_backend.tap(400, 220)
        except io_backend.ADBError as exc:
            print(f"[ADB ERROR] {exc}")
            break
        time.sleep(1.5)
        if tienda_utils.tienda_presente():
            break

    time.sleep(2)


def train_loop(
    total_steps: int = 1000,
    train_interval: int = 4,
    save_interval: int = 100,
    model_path: str = MODEL_PATH,
) -> None:
    """Run the main training loop."""

    init_state = leer_estado_juego()
    state_vec = vector_entrada(init_state)

    agent = DQNAgent(len(state_vec), 5)

    if os.path.exists(model_path):
        agent.policy_net.load_state_dict(torch.load(model_path))
        agent.target_net.load_state_dict(agent.policy_net.state_dict())
        print(f"[INFO] Modelo cargado desde {model_path}")

    current_state_dict = init_state
    current_state = state_vec

    for step in range(1, total_steps + 1):
        action = agent.select_action(current_state)
        _ejecutar_accion(action)
        time.sleep(0.5)

        next_state_dict = leer_estado_juego()
        fin, gano = detectar_fin_partida()
        if fin:
            next_state_dict["gano"] = gano
        next_state = vector_entrada(next_state_dict)

        reward = _calcular_recompensa(current_state_dict, next_state_dict)
        done = fin

        agent.remember((current_state, action, reward, next_state, done))

        if step % train_interval == 0:
            agent.train_step()

        if step % save_interval == 0:
            torch.save(agent.policy_net.state_dict(), model_path)
            print(f"[INFO] Modelo guardado en {model_path} (paso {step})")

        if done:
            _reiniciar_partida()
            current_state_dict = leer_estado_juego()
            current_state = vector_entrada(current_state_dict)
        else:
            current_state_dict = next_state_dict
            current_state = next_state


if __name__ == "__main__":
    train_loop()
