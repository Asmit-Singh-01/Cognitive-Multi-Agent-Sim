import numpy as np

class CognitiveAgent:
    def __init__(self, id):
        self.id = id
        self.pos = np.random.rand(2) * 100
        self.energy = 100
        self.memory = np.zeros(5) # Cognitive Memory
        
    def step(self, strategy):
        # Stochastic Strategy: Agents change behavior based on memory
        if strategy == "greedy":
            self.pos += np.random.randn(2) * 2
            self.energy -= 1
        else: # Cooperative
            self.pos += np.random.randn(2) * 0.5
            self.energy -= 0.2

class SimulationEngine:
    def __init__(self, num_agents=10):
        self.agents = [CognitiveAgent(i) for i in range(num_agents)]
        
    def update(self):
        for agent in self.agents:
            # Cognitive decision logic
            strategy = "greedy" if agent.energy > 50 else "cooperative"
            agent.step(strategy)
            
        return np.array([a.pos for a in self.agents])
      
