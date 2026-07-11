import numpy as np
from environment import CognitiveMultiAgentEnv
from dqn_agent import MultiAgentDQN

def main():
    # 1. Environment Setup (Chhota grid jaldi seekhne ke liye)
    env = CognitiveMultiAgentEnv(grid_size=6, num_agents=2, num_resources=2)
    state_dim = env.observation_space.shape[0]
    action_dim = env.action_space.n

    # 2. Agents Setup (Har agent ko apna apna DQN dimaag de rahe hain)
    agents = [MultiAgentDQN(state_dim, action_dim) for _ in range(env.num_agents)]

    episodes = 200 # Kitni baar environment reset hoke shuru hoga
    batch_size = 32
    max_steps_per_episode = 50 

    print("Training shuru ho rahi hai... 🚀\n")

    # 3. Main Training Loop
    for ep in range(episodes):
        state, _ = env.reset()
        total_rewards = np.zeros(env.num_agents)
        step_count = 0
        
        while step_count < max_steps_per_episode:
            step_count += 1
            
            # Har agent current state dekh kar apna action sochega
            actions = []
            for i in range(env.num_agents):
                action = agents[i].act(state)
                actions.append(action)
                
            # Environment me wo actions perform honge
            next_state, rewards, terminated, truncated, _ = env.step(actions)
            
            # Har agent apni memory me experience save karega aur train hoga
            for i in range(env.num_agents):
                # Format: (state, action, reward, next_state, done)
                agents[i].remember(state, actions[i], rewards[i], next_state, terminated)
                agents[i].train_step(batch_size)
                
                total_rewards[i] += rewards[i]
                
            # Agle step ke liye state update karo
            state = next_state
            
            if terminated or truncated:
                break
                
        # Har 10 episode ke baad "Target Network" ko update karo (Stability ke liye)
        if ep % 10 == 0:
            for agent in agents:
                agent.target_network.load_state_dict(agent.q_network.state_dict())
                
        # Har 20 episode ke baad result print karo taaki hum progress dekh sakein
        if (ep + 1) % 20 == 0:
            print(f"Episode: {ep + 1}/{episodes} | "
                  f"Randomness (Epsilon): {agents[0].epsilon:.2f} | "
                  f"Rewards: {total_rewards}")

    print("\nTraining Complete! ✅")

if __name__ == "__main__":
    main()
  
