from environment import CognitiveMultiAgentEnv
import numpy as np

# Init environment
env = CognitiveMultiAgentEnv(grid_size=6, num_agents=2, num_resources=2)
obs, info = env.reset()

print("Initial Environment State:")
env.render()

# Take 3 random steps to test
for step in range(3):
    # Generate random actions for both agents
    random_actions = [env.action_space.sample() for _ in range(env.num_agents)]
    obs, rewards, terminated, truncated, info = env.step(random_actions)
    
    print(f"Step {step + 1} | Actions taken: {random_actions} | Rewards: {rewards}")
    env.render()
  
