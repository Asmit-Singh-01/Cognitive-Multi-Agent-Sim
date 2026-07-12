import numpy as np

class CognitiveProcessor:
    """
    Introduces cognitive biases and 'Theory of Mind' concepts into standard RL decisions.
    Demonstrates the limitation of pure mathematical RL when facing human-like uncertainty.
    """
    def __init__(self, agent_id, risk_tolerance=0.5):
        self.agent_id = agent_id
        # Human decision making is often not purely rational.
        # risk_tolerance determines how bold or cautious the agent is when predicting others.
        self.risk_tolerance = risk_tolerance
        
    def estimate_other_agents_intent(self, my_pos, other_agents_pos, resources):
        """
        Agent tries to guess what other agents are going to do based on proximity to resources.
        (A basic form of Theory of Mind)
        """
        predicted_moves = []
        for other_pos in other_agents_pos:
            # Find the closest resource to the other agent
            closest_res = None
            min_dist = float('inf')
            
            for res in resources:
                dist = np.linalg.norm(np.array(other_pos) - np.array(res))
                if dist < min_dist:
                    min_dist = dist
                    closest_res = res
                    
            # The agent "assumes" the other agent will go for its closest resource
            if closest_res is not None:
                predicted_moves.append(closest_res)
                
        return predicted_moves

    def apply_cognitive_bias(self, raw_q_values, predicted_conflicts):
        """
        Modifies raw Q-values from the DQN based on predicted conflicts.
        If an agent thinks another agent is going for the same resource, 
        a cautious agent might back off (sub-optimal mathematically, but human-like).
        """
        # We will integrate this logic into the action selection phase later.
        # For now, it returns the raw values or slightly dampened values if conflict is high.
        
        conflict_penalty = 0.0
        if len(predicted_conflicts) > 0:
            # Simple bias: if it senses conflict, it reduces the value of aggressive actions
            conflict_penalty = (1.0 - self.risk_tolerance) * 0.2
            
        # Dampen the highest Q-value slightly to simulate hesitation
        adjusted_q_values = raw_q_values.clone()
        if conflict_penalty > 0:
            max_idx = np.argmax(adjusted_q_values.cpu().detach().numpy())
            adjusted_q_values[0][max_idx] -= conflict_penalty
            
        return adjusted_q_values

# Test the processor
if __name__ == "__main__":
    cog = CognitiveProcessor(agent_id=0, risk_tolerance=0.3)
    print("Cognitive Module Initialized.")
  
