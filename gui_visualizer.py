import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from engine import SimulationEngine

engine = SimulationEngine()
fig, ax = plt.subplots(figsize=(8, 6))

def update(frame):
    ax.clear()
    positions = engine.update()
    ax.scatter(positions[:,0], positions[:,1], c='cyan', s=50)
    ax.set_xlim(0, 100); ax.set_ylim(0, 100)
    ax.set_title(f"Live Cognitive Simulation - Step {frame}")

ani = FuncAnimation(fig, update, frames=200, interval=50)
plt.show()
