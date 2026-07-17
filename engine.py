import numpy as np
import requests

# C++ physics module ko load karne ki koshish (Fallback implementation)
try:
    import physics_core
    CPP_AVAILABLE = True
except ImportError:
    CPP_AVAILABLE = False

class CognitiveAgent:
    def __init__(self, id):
        self.id = id
        self.pos = np.random.rand(2) * 100
        self.energy = 100
        self.memory = np.zeros(5) # Cognitive Memory
        
    def step(self, strategy):
        # Default Python movement logic (Sirf tab chalega jab C++ engine compiled na ho)
        if strategy == "greedy":
            self.pos += np.random.randn(2) * 2.5
            self.energy -= 1.5
        else: # Cooperative
            self.pos += np.random.randn(2) * 0.8
            self.energy -= 0.3

        # Grid ki boundary se baahar na jaane dena
        self.pos = np.clip(self.pos, 0, 100)

class SimulationEngine:
    def __init__(self, num_agents=10):
        self.agents = [CognitiveAgent(i) for i in range(num_agents)]
        self.step_count = 0
        self.gateway_url = "http://localhost:8080/telemetry"
        
        # C++ engine initiate karna agar compiled binary present hai
        if CPP_AVAILABLE:
            self.physics = physics_core.PhysicsEngine()
            print("[+] High-Performance C++ Physics Engine Connected!")
        else:
            self.physics = None
            print("[-] C++ Engine not compiled. Running via Native Python fallback mode.")
            
    def update(self):
        self.step_count += 1
        
        # Ek saath saare agents ke coordinates aur unki strategy extract karna
        current_positions = np.array([agent.pos for agent in self.agents])
        strategies = ["greedy" if agent.energy > 50 else "cooperative" for agent in self.agents]
        
        if CPP_AVAILABLE and self.physics is not None:
            # ⚡ HIGH-SPEED C++ MODE
            next_positions = self.physics.update_positions(current_positions, strategies)
            for i, agent in enumerate(self.agents):
                agent.pos = next_positions[i]
                # Energy manually deplete karna python level par
                if strategies[i] == "greedy":
                    agent.energy -= 1.5
                else:
                    agent.energy -= 0.3
        else:
            # 🐍 PYTHON FALLBACK MODE
            for i, agent in enumerate(self.agents):
                agent.step(strategies[i])
            
        # Go Gateway ko telemetry packets stream karna
        for agent in self.agents:
            strategy = "greedy" if agent.energy > 50 else "cooperative"
            payload = {
                "step": self.step_count,
                "agent_id": agent.id,
                "energy": float(agent.energy),
                "strategy": strategy,
                "x": float(agent.pos[0]),
                "y": float(agent.pos[1])
            }
            
            try:
                # Minimal latency pipeline ke liye low timeout limit
                requests.post(self.gateway_url, json=payload, timeout=0.01)
            except requests.exceptions.RequestException:
                pass
                
        return np.array([agent.pos for agent in self.agents])
        
