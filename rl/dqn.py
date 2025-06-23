import random
from collections import deque
from typing import List, Tuple

import torch
import torch.nn as nn
import torch.optim as optim


class ReplayBuffer:
    """Circular buffer for storing transitions."""

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.buffer: deque = deque(maxlen=capacity)

    def __len__(self) -> int:
        return len(self.buffer)

    def push(self, transition: Tuple[List[float], int, float, List[float], bool]) -> None:
        self.buffer.append(transition)

    def sample(self, batch_size: int):
        indices = random.sample(range(len(self.buffer)), batch_size)
        batch = [self.buffer[i] for i in indices]
        states, actions, rewards, next_states, dones = zip(*batch)
        return (
            torch.tensor(states, dtype=torch.float32),
            torch.tensor(actions, dtype=torch.long),
            torch.tensor(rewards, dtype=torch.float32),
            torch.tensor(next_states, dtype=torch.float32),
            torch.tensor(dones, dtype=torch.bool),
        )


class DQNAgent:
    """Double DQN agent with target network and replay buffer."""

    def __init__(
        self,
        state_size: int,
        action_size: int,
        lr: float = 1e-3,
        gamma: float = 0.99,
        buffer_size: int = 10000,
        batch_size: int = 32,
        target_update_freq: int = 100,
    ) -> None:
        self.action_size = action_size
        self.gamma = gamma
        self.batch_size = batch_size
        self.epsilon = 1.0
        self.epsilon_min = 0.1
        self.epsilon_decay = 0.995
        self.learn_step = 0
        self.target_update_freq = target_update_freq

        self.policy_net = nn.Sequential(
            nn.Linear(state_size, 64),
            nn.ReLU(),
            nn.Linear(64, action_size),
        )
        self.target_net = nn.Sequential(
            nn.Linear(state_size, 64),
            nn.ReLU(),
            nn.Linear(64, action_size),
        )
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()

        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=lr)
        self.loss_fn = nn.SmoothL1Loss()

        self.memory = ReplayBuffer(buffer_size)

    def select_action(self, state: List[float]) -> int:
        if random.random() < self.epsilon:
            return random.randrange(self.action_size)
        with torch.no_grad():
            state_t = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
            q_values = self.policy_net(state_t)
            return int(torch.argmax(q_values))

    def remember(self, transition: Tuple[List[float], int, float, List[float], bool]) -> None:
        self.memory.push(transition)

    def train_step(self) -> None:
        if len(self.memory) < self.batch_size:
            return

        states, actions, rewards, next_states, dones = self.memory.sample(self.batch_size)

        q_values = self.policy_net(states).gather(1, actions.unsqueeze(1)).squeeze()

        with torch.no_grad():
            next_actions = self.policy_net(next_states).argmax(1)
            next_q_values = self.target_net(next_states).gather(1, next_actions.unsqueeze(1)).squeeze()
            target_q = rewards + (~dones) * self.gamma * next_q_values

        loss = self.loss_fn(q_values, target_q)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

        self.learn_step += 1
        if self.learn_step % self.target_update_freq == 0:
            self.target_net.load_state_dict(self.policy_net.state_dict())

