"""Main training loop using the DQN agent."""

import os
import time

import torch

import io_backend
from leer_estado_juego import leer_estado_juego
from preparar_datos import vector_entrada
from rl.dqn import DQNAgent


MODEL_PATH = "dqn_model.pth"


def _ejecutar_accion(indice: int) -> None:
    """Placeholder to interact with the game.

    In a real scenario this should trigger the click/tap on the
    corresponding hero slot. For now it simply prints the action so the
    loop can run without an actual device.
    """

    print(f"[ACTION] Comprar en slot {indice}")


def _calcular_recompensa(prev_state: dict, next_state: dict) -> float:
    """Simple reward based on the change of gold between states."""

    oro_prev = prev_state.get("oro", 0) or 0
    oro_next = next_state.get("oro", 0) or 0
    return float(oro_next - oro_prev)


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
        next_state = vector_entrada(next_state_dict)

        reward = _calcular_recompensa(current_state_dict, next_state_dict)
        done = False

        agent.remember((current_state, action, reward, next_state, done))

        if step % train_interval == 0:
            agent.train_step()

        if step % save_interval == 0:
            torch.save(agent.policy_net.state_dict(), model_path)
            print(f"[INFO] Modelo guardado en {model_path} (paso {step})")

        current_state_dict = next_state_dict
        current_state = next_state


if __name__ == "__main__":
    train_loop()
