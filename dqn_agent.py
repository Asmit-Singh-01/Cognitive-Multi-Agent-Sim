import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
from collections import deque

# 1. The Neural Network (Brain of the Agent)
class DQN(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(DQN, self).__init__()
        # Fast, feed-forward architecture
        self.network = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, output_dim)
        )

    def forward(self, x):
        return self.network(x)

# 2. Multi-Agent Logic & Training Engine
class MultiAgentDQN:
    def __init__(self, state_dim, action_dim, lr=1e-3, gamma=0.99, epsilon=1.0, epsilon_decay=0.995, min_epsilon=0.01):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.gamma = gamma # Discount factor for future rewards
        
        # Exploration vs Exploitation params
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon
        
        # Q-Network aur Target Network initialize karna
        self.q_network = DQN(state_dim, action_dim)
        self.target_network = DQN(state_dim, action_dim)
        self.target_network.load_state_dict(self.q_network.state_dict())
        
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=lr)
        self.memory = deque(maxlen=10000) # Replay Buffer
        
    def act(self, state):
        # Random action chuno agar epsilon high hai (Exploration)
        if random.random() < self.epsilon:
            return random.randint(0, self.action_dim - 1)
        
        # Model se best action lo (Exploitation)
        state_tensor = torch.FloatTensor(state).unsqueeze(0)
        with torch.no_grad():
            q_values = self.q_network(state_tensor)
        return torch.argmax(q_values).item()

    def remember(self, state, action, reward, next_state, done):
        # Experience ko memory me save karo
        self.memory.append((state, action, reward, next_state, done))

    def train_step(self, batch_size=32):
        if len(self.memory) < batch_size:
            return
        
        # Memory se random batch uthao training ke liye
        batch = random.sample(self.memory, batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        
        # Convert to PyTorch Tensors
        states = torch.FloatTensor(np.array(states))
        actions = torch.LongTensor(actions).unsqueeze(1)
        rewards = torch.FloatTensor(rewards).unsqueeze(1)
        next_states = torch.FloatTensor(np.array(next_states))
        dones = torch.FloatTensor(dones).unsqueeze(1)
        
        # Current Q values
        current_q = self.q_network(states).gather(1, actions)
        
        # Target Q values
        with torch.no_grad():
            max_next_q = self.target_network(next_states).max(1)[0].unsqueeze(1)
            target_q = rewards + self.gamma * max_next_q * (1 - dones)
            
        # Loss calculate karke backpropagate karo
        loss = nn.MSELoss()(current_q, target_q)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        # Epsilon (randomness) ko dreere-dheere kam karo
        if self.epsilon > self.min_epsilon:
            self.epsilon *= self.epsilon_decay
          
