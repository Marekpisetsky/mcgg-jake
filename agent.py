import random
from typing import List, Tuple

import torch
import torch.nn as nn
import torch.optim as optim


class Agent:
    """Agente simple basado en DQN.

    Mantiene un modelo de política, registra recompensas y
    actualiza la red con Q-learning de una sola etapa.
    """

    def __init__(self, state_size: int, action_size: int, lr: float = 1e-3,
                 gamma: float = 0.99) -> None:
        self.action_size = action_size
        self.gamma = gamma
        self.epsilon = 1.0
        self.epsilon_min = 0.1
        self.epsilon_decay = 0.995
        self.rewards: List[float] = []

        self.policy_net = nn.Sequential(
            nn.Linear(state_size, 64),
            nn.ReLU(),
            nn.Linear(64, action_size)
        )
        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=lr)
        self.loss_fn = nn.MSELoss()

    def select_action(self, state: List[float]) -> int:
        """Devuelve la acción a tomar usando una estrategia epsilon-greedy."""
        if random.random() < self.epsilon:
            return random.randrange(self.action_size)
        with torch.no_grad():
            state_t = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
            q_values = self.policy_net(state_t)
            return int(torch.argmax(q_values))

    def update_policy(self, transition: Tuple[List[float], int, float,
                                              List[float], bool]) -> None:
        """Actualiza la política usando Q-learning simple."""
        state, action, reward, next_state, done = transition
        self.rewards.append(reward)

        state_t = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
        next_state_t = torch.tensor(next_state, dtype=torch.float32).unsqueeze(0)
        reward_t = torch.tensor(reward, dtype=torch.float32)

        q_values = self.policy_net(state_t)
        next_q_values = self.policy_net(next_state_t)

        target = reward_t
        if not done:
            target = reward_t + self.gamma * next_q_values.max().detach()

        loss = self.loss_fn(q_values[0, action], target)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
