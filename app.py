import streamlit as st
import plotly.graph_objects as go
import numpy as np
import time

# Page configuration
st.set_page_config(layout="wide", page_title="Cognitive Sim v2")

# 1. SESSION STATE INITIALIZATION (For Start, Stop, Resume tracking)
if 'current_step' not in st.session_state:
    st.session_state.current_step = 20  # Starting from your sample step
if 'sim_running' not in st.session_state:
    st.session_state.sim_running = False

st.title("🧠 Cognitive Multi-Agent Control Center")

# --- SIDEBAR / CONTROLS SECTION ---
st.subheader("🎛️ Simulation Controls")
col_ctrl1, col_ctrl2, col_ctrl3, col_style = st.columns([15, 15, 15, 55])

with col_ctrl1:
    if st.button("▶️ Start / Resume", use_container_width=True):
        st.session_state.sim_running = True

with col_ctrl2:
    if st.button("⏸️ Pause / Stop", use_container_width=True):
        st.session_state.sim_running = False

with col_ctrl3:
    if st.button("🔄 Reset", use_container_width=True):
        st.session_state.current_step = 0
        st.session_state.sim_running = False
        st.rerun()

with col_style:
    # Multiple Graph Styles Dropdown
    graph_style = st.selectbox(
        "📊 Choose Visualization Style:",
        ["2D Interactive Grid", "3D Cognitive Space (Scatter3D)", "3D Energy Terrain (Mesh/Surface)"]
    )

st.markdown("---")

# --- MAIN LAYOUT ---
col_graph, col_metrics = st.columns([70, 30])

# Dummy data generator based on steps (Replace this with your C++/Go backend data fetch)
np.random.seed(42)
num_agents = 50
x_data = np.random.randint(0, 100, num_agents)
y_data = np.random.randint(0, 100, num_agents)
# Z-axis representing Energy Levels for 3D view
z_data = np.random.uniform(-1.2, -0.2, num_agents) 

with col_graph:
    st.write(### `Visualization Area`)
    fig = go.Figure()

    # 2. MULTIPLE GRAPH STYLES LOGIC
    if graph_style == "2D Interactive Grid":
        fig.add_trace(go.Scatter(
            x=x_data, y=y_data, 
            mode='markers',
            marker=dict(size=10, color=z_data, colorscale='Viridis', showscale=True, title="Energy")
        ))
        fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=350, template="plotly_dark")

    elif graph_style == "3D Cognitive Space (Scatter3D)":
        # 3D Scatter Plot for Agents
        fig.add_trace(go.Scatter3d(
            x=x_data, y=y_data, z=z_data,
            mode='markers',
            marker=dict(size=6, color=z_data, colorscale='Cividis', opacity=0.8)
        ))
        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0), 
            height=350, 
            template="plotly_dark",
            scene=dict(
                xaxis_title='X Path',
                yaxis_title='Y Path',
                zaxis_title='Energy Friction'
            )
        )

    elif graph_style == "3D Energy Terrain (Mesh/Surface)":
        # 3D Mesh/Surface plot to show system density
        fig.add_trace(go.Mesh3d(
            x=x_data, y=y_data, z=z_data,
            opacity=0.6, colorscale='Hot'
        ))
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=350, template="plotly_dark")

    st.plotly_chart(fig, use_container_width=True)

with col_metrics:
    st.write(### `Live Telemetry`)
    st.metric("Active Live Agents", f"{num_agents} / 50")
    st.metric("Engine Current Step", f"{st.session_state.current_step} / 200")
    
    # Simple status indicator
    if st.session_state.sim_running:
        st.success("🟢 Simulation Running...")
    else:
        st.warning("⏸️ Simulation Paused")

# 3. STATEFUL LOOP (Resumes exactly where it stopped)
if st.session_state.sim_running and st.session_state.current_step < 200:
    time.sleep(0.5)  # Controlling fluid updates
    st.session_state.current_step += 5  # Incrementing steps
    st.rerun()
