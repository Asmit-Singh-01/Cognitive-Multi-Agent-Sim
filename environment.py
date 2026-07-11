import numpy as np
import gymnasium as gym
from gymnasium import spaces

class CognitiveMultiAgentEnv(gym.Env):
    """
    Custom Multi-Agent Grid World Environment.
    Agents need to collect resources while avoiding collisions.
    """
    def __init__(self, grid_size=10, num_agents=2, num_resources=3):
        super(CognitiveMultiAgentEnv, self).__init__()
        
        self.grid_size = grid_size
        self.num_agents = num_agents
        self.num_resources = num_resources
        
        # Actions: 0=Up, 1=Down, 2=Left, 3=Right, 4=Stay
        self.action_space = spaces.Discrete(5)
        
        # Observation space: Positions of all agents and resources
        # Represented as a flattened array for simplicity
        self.observation_space = spaces.Box(
            low=0, high=grid_size-1, 
            shape=(num_agents * 2 + num_resources * 2,), 
            dtype=np.int32
        )
        
        self.reset()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        
        # Randomly place agents
        self.agent_positions = np.random.randint(0, self.grid_size, size=(self.num_agents, 2))
        
        # Randomly place resources
        self.resource_positions = np.random.randint(0, self.grid_size, size=(self.num_resources, 2))
        
        return self._get_obs(), {}

    def _get_obs(self):
        return np.concatenate([self.agent_positions.flatten(), self.resource_positions.flatten()])

    def step(self, actions):
        """
        actions: list or array of integers representing action for each agent
        """
        rewards = np.zeros(self.num_agents)
        terminated = False
        truncated = False
        
        # Update agent positions based on actions
        for i, action in enumerate(actions):
            if action == 0 and self.agent_positions[i][0] > 0: # Up
                self.agent_positions[i][0] -= 1
            elif action == 1 and self.agent_positions[i][0] < self.grid_size - 1: # Down
                self.agent_positions[i][0] += 1
            elif action == 2 and self.agent_positions[i][1] > 0: # Left
                self.agent_positions[i][1] -= 1
            elif action == 3 and self.agent_positions[i][1] < self.grid_size - 1: # Right
                self.agent_positions[i][1] += 1
                
        # Reward calculation: Check if any agent reached a resource
        for i, agent_pos in enumerate(self.agent_positions):
            for j, res_pos in enumerate(self.resource_positions):
                if np.array_equal(agent_pos, res_pos):
                    rewards[i] += 10  # High reward for collecting resource
                    # Relocate resource after collection
                    self.resource_positions[j] = np.random.randint(0, self.grid_size, size=(2,))
                    
            # Small step penalty to encourage efficiency
            rewards[i] -= 0.1
            
        # Collision penalty between agents
        for i in range(self.num_agents):
            for j in range(i + 1, self.num_agents):
                if np.array_equal(self.agent_positions[i], self.agent_positions[j]):
                    rewards[i] -= 5
                    rewards[j] -= 5
                    
        obs = self._get_obs()
        info = {}
        
        return obs, rewards, terminated, truncated, info

    def render(self):
        # A simple text-based rendering for mobile/console logs
        grid = np.full((self.grid_size, self.grid_size), '.')
        for res in self.resource_positions:
            grid[res[0], res[1]] = 'R'
        for idx, agent in enumerate(self.agent_positions):
            grid[agent[0], agent[1]] = f'A{idx}'
            
        print("\n".join([" ".join(row) for row in grid]))
        print("-" * (self.grid_size * 2))
      
