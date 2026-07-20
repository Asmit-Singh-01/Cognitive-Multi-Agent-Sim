import streamlit as st
import plotly.graph_objects as go
import numpy as np
import time

# Page setup
st.set_page_config(layout="wide", page_title="Cognitive Multi-Agent Control Center")

# 1. SESSION STATE INITIALIZATION
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0
if 'sim_running' not in st.session_state:
    st.session_state.sim_running = False

st.title("🧠 Cognitive Multi-Agent Control Center")

# 2. CONTROLS SECTION
st.subheader("🎮 Simulation Controls")
col_ctrl1, col_ctrl2, col_ctrl3, col_styles = st.columns([15, 15, 15, 55])

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

with col_styles:
    graph_style = st.selectbox(
        "Choose Visualization Style:",
        ["2D Interactive Grid", "3D Cognitive Space (Scatter3D)", "3D Energy Terrain (Mesh/Surface)"]
    )

st.markdown("---")

# 3. DYNAMIC MULTI-AGENT STATE GENERATION
num_agents = 50
step = st.session_state.current_step

# Base positions
np.random.seed(42)
base_x = np.random.uniform(10, 90, num_agents)
base_y = np.random.uniform(10, 90, num_agents)

# Dynamic trajectory & continuous state evolution per step
time_factor = step / 15.0
x_data = np.clip(base_x + 12 * np.sin(time_factor + np.arange(num_agents)), 0, 100)
y_data = np.clip(base_y + 12 * np.cos(time_factor * 0.8 + np.arange(num_agents)), 0, 100)

# Energy levels dynamically evolving over steps (-1.0 to +0.5 range)
energy_data = np.sin(time_factor + (x_data + y_data) / 25.0) * 0.7 - 0.25
energy_data = np.clip(energy_data, -1.0, 0.5)

# 4. VISUALIZATION AREA
st.subheader("Visualization Area")
fig = go.Figure()

if graph_style == "2D Interactive Grid":
    fig.add_trace(go.Scatter(
        x=x_data,
        y=y_data,
        mode='markers',
        marker=dict(
            size=12,
            color=energy_data,
            colorscale='Viridis',
            colorbar=dict(title="Energy"),
            cmin=-1.0,
            cmax=0.5,
            showscale=True
        )
    ))
    fig.update_layout(
        xaxis=dict(range=[0, 100], title="X Position"),
        yaxis=dict(range=[0, 100], title="Y Position"),
        margin=dict(l=20, r=20, t=30, b=20),
        height=500
    )

elif graph_style == "3D Cognitive Space (Scatter3D)":
    fig.add_trace(go.Scatter3d(
        x=x_data,
        y=y_data,
        z=energy_data,
        mode='markers',
        marker=dict(
            size=6,
            color=energy_data,
            colorscale='Cividis',
            colorbar=dict(title="Energy Level"),
            cmin=-1.0,
            cmax=0.5
        )
    ))
    fig.update_layout(
        scene=dict(
            xaxis_title='X Position',
            yaxis_title='Y Position',
            zaxis_title='Energy Friction'
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=500
    )

elif graph_style == "3D Energy Terrain (Mesh/Surface)":
    grid_x, grid_y = np.meshgrid(np.linspace(0, 100, 30), np.linspace(0, 100, 30))
    grid_z = np.sin(grid_x / 15.0 + time_factor) * np.cos(grid_y / 15.0 + time_factor) * 0.5
    
    fig.add_trace(go.Surface(
        x=grid_x,
        y=grid_y,
        z=grid_z,
        colorscale='Hot',
        colorbar=dict(title="Energy Density")
    ))
    fig.update_layout(
        scene=dict(
            xaxis_title='X Grid',
            yaxis_title='Y Grid',
            zaxis_title='Energy Surface'
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=500
    )

st.plotly_chart(fig, use_container_width=True)

# 5. LIVE TELEMETRY
st.subheader("Live Telemetry")
col_tel1, col_tel2 = st.columns(2)
col_tel1.metric("Active Live Agents", f"{num_agents} / 50")
col_tel2.metric("Engine Current Step", f"{st.session_state.current_step} / 200")

if st.session_state.sim_running and st.session_state.current_step < 200:
    st.success("🟢 Simulation Running...")
    time.sleep(0.08)
    st.session_state.current_step += 1
    st.rerun()
elif st.session_state.current_step >= 200:
    st.warning("⏸️ Simulation Completed (200/200 Steps)")
else:
    st.warning("⏸️ Simulation Paused")
    
