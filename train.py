import numpy as np
import requests  # Go server se baat karne ke liye
from environment import CognitiveMultiAgentEnv
from dqn_agent import MultiAgentDQN
from cognitive_logic import CognitiveProcessor

GO_GATEWAY_URL = "http://localhost:8080/update"

def log_to_go_gateway(agent_id, position, action, bias_level):
    """Sends real-time agent telemetry to the High-Throughput Go Server"""
    payload = {
        "agent_id": int(agent_id),
        "position": [float(pos) for pos in position],
        "action": int(action),
        "cognitive_bias_level": float(bias_level)
    }
    try:
        # We use a short timeout so simulation doesn't hang if server is busy
        requests.post(GO_GATEWAY_URL, json=payload, timeout=0.01)
    except requests.exceptions.RequestException:
        # Agar Go server abhi running nahi hai, toh simulation rukegi nahi
        pass

def main():
    env = CognitiveMultiAgentEnv(grid_size=6, num_agents=2, num_resources=2)
    state_dim = env.observation_space.shape[0]
    action_dim = env.action_space.n

    agents = [MultiAgentDQN(state_dim, action_dim) for _ in range(env.num_agents)]
    
    # Human-like Cognitive processors for both agents
    cognitive_brains = [CognitiveProcessor(agent_id=i, risk_tolerance=0.4) for i in range(env.num_agents)]

    episodes = 200
    batch_size = 32
    max_steps_per_episode = 50 

    print("Advanced Multi-Language Training Initiated... 🚀\n")

    for ep in range(episodes):
        state, _ = env.reset()
        total_rewards = np.zeros(env.num_agents)
        step_count = 0
        
        while step_count < max_steps_per_episode:
            step_count += 1
            actions = []
            
            # Extract current positions for cognitive processing
            # (First 4 elements of state are agent positions in our env setup)
            agent_positions = [env.agent_positions[i] for i in range(env.num_agents)]
            resource_positions = env.resource_positions
            
            for i in range(env.num_agents):
                action = agents[i].act(state)
                actions.append(action)
                
                # Real-time Telemetry: Send data to Go Engine pipeline
                log_to_go_gateway(
                    agent_id=i, 
                    position=agent_positions[i], 
                    action=action, 
                    bias_level=cognitive_brains[i].risk_tolerance
                )
                
            next_state, rewards, terminated, truncated, _ = env.step(actions)
            
            for i in range(env.num_agents):
                agents[i].remember(state, actions[i], rewards[i], next_state, terminated)
                agents[i].train_step(batch_size)
                total_rewards[i] += rewards[i]
                
            state = next_state
            if terminated or truncated:
                break
                
        if ep % 10 == 0:
            for agent in agents:
                agent.target_network.load_state_dict(agent.q_network.state_dict())
                
        if (ep + 1) % 20 == 0:
            print(f"Episode: {ep + 1}/{episodes} | Rewards: {total_rewards} | Telemetry streaming active.")

    print("\nSystem Execution Complete! ✅")

if __name__ == "__main__":
    main()
    
