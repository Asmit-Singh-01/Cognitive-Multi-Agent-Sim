import numpy as np
import requests

class CognitiveAgent:
    def __init__(self, id):
        self.id = id
        self.pos = np.random.rand(2) * 100
        self.energy = 100
        self.memory = np.zeros(5) # Cognitive Memory
        
    def step(self, strategy):
        # Stochastic Strategy: Agents change behavior based on energy
        if strategy == "greedy":
            self.pos += np.random.randn(2) * 2.5
            self.energy -= 1.5
        else: # Cooperative
            self.pos += np.random.randn(2) * 0.8
            self.energy -= 0.3

class SimulationEngine:
    def __init__(self, num_agents=10):
        self.agents = [CognitiveAgent(i) for i in range(num_agents)]
        self.step_count = 0
        self.gateway_url = "http://localhost:8080/telemetry"
        
    def update(self):
        self.step_count += 1
        positions = []
        
        for agent in self.agents:
            strategy = "greedy" if agent.energy > 50 else "cooperative"
            agent.step(strategy)
            positions.append(agent.pos)
            
            # Go Telemetry Gateway ko data stream karna
            payload = {
                "step": self.step_count,
                "agent_id": agent.id,
                "energy": float(agent.energy),
                "strategy": strategy,
                "x": float(agent.pos[0]),
                "y": float(agent.pos[1])
            }
            
            try:
                # Non-blocking feel dene ke liye low timeout set kiya hai
                requests.post(self.gateway_url, json=payload, timeout=0.01)
            except requests.exceptions.RequestException:
                # Agar Go Gateway running nahi hai toh bina crash kiye simulation chalta rahega
                pass
            
        return np.array(positions)
        
