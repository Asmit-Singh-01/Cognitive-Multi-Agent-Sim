import streamlit as st
import numpy as np
import plotly.graph_objects as go
from engine import SimulationEngine
import time

# Page config for high-end web app feel
st.set_page_config(page_title="Cognitive Multi-Agent Sim Dashboard", layout="wide")

st.title("🧠 Cognitive Multi-Agent Simulation Dashboard")
st.markdown("---")

# Sidebar Controls
st.sidebar.header("⚙️ Simulation Environment Controls")
num_agents = st.sidebar.slider("Total AI Agents", min_value=5, max_value=50, value=15, step=5)
sim_speed = st.sidebar.slider("Simulation Delay (Seconds)", min_value=0.01, max_value=0.5, value=0.1)
total_steps = st.sidebar.slider("Total Simulation Steps", min_value=50, max_value=200, value=100, step=50)

start_sim = st.sidebar.button("▶️ Launch Simulation")

# Layout Split: Left for Visual Map, Right for Production Analytics
col1, col2 = st.columns([2, 1])

if 'engine' not in st.session_state:
    st.session_state.engine = SimulationEngine(num_agents=num_agents)

with col1:
    st.subheader("📊 Live Interactive Agent Grid")
    plot_placeholder = st.empty()

with col2:
    st.subheader("📡 Real-Time Telemetry Performance")
    metrics_placeholder = st.empty()

# Run the simulation loop when button is clicked
if start_sim:
    # Reset engine for clean state
    st.session_state.engine = SimulationEngine(num_agents=num_agents)
    
    for step in range(total_steps):
        positions = st.session_state.engine.update()
        
        # Gathering metrics from the engine instance
        strategies = ["greedy" if a.energy > 50 else "cooperative" for a in st.session_state.engine.agents]
        energies = [a.energy for a in st.session_state.engine.agents]
        avg_energy = np.mean(energies)
        
        # Creating an interactive Plotly Scatter plot (Hover support included)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=positions[:, 0], y=positions[:, 1],
            mode='markers',
            marker=dict(
                size=14,
                color=energies, 
                colorscale='Cividis', 
                showscale=True,
                colorbar=dict(title="Energy Level"),
                line=dict(width=1, color='white')
            ),
            text=[f"Agent ID: {i}<br>Strategy: {s.upper()}<br>Energy: {e:.1f}" for i, (s, e) in enumerate(zip(strategies, energies))],
            hoverinfo='text'
        ))
        
        fig.update_layout(
            xaxis=dict(range=[0, 100], gridcolor='#2c2c2c'),
            yaxis=dict(range=[0, 100], gridcolor='#2c2c2c'),
            template="plotly_dark",
            margin=dict(l=10, r=10, t=10, b=10),
            height=500,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        # Update Web UI components dynamically
        plot_placeholder.plotly_chart(fig, use_container_width=True)
        
        with metrics_placeholder.container():
            st.metric(label="🟢 Active Live Agents", value=f"{num_agents} / {num_agents}")
            st.metric(label="⚡ System Mean Energy", value=f"{avg_energy:.2f}%")
            st.metric(label="🔄 Engine Current Step", value=f"{step + 1} / {total_steps}")
            st.success("📡 Go Telemetry Core: Connected (Port 8080)")
            
        time.sleep(sim_speed)
      
