# 🧠 Cognitive-Multi-Agent-Sim.

![Status](https://img.shields.io/badge/Status-Active_Development-brightgreen?style=flat-square)
![Tech](https://img.shields.io/badge/Tech-Python_%7C_PyTorch_%7C_Gymnasium-blue?style=flat-square)
![Backend](https://img.shields.io/badge/Engine-C%2B%2B_%7C_Go%2F%20Golang-orange?style=flat-square)
![CI/CD](https://img.shields.io/badge/Build-Passing-green?style=flat-square)

Welcome to **Cognitive-Multi-Agent-Sim**! 🚀

## 🎯 About The Project
This project is a custom-built, dynamic simulation environment where multiple AI entities (agents) learn to coordinate, plan complex tasks, and survive—**entirely without human instruction.** 

Using Deep Reinforcement Learning (DRL), this simulation forces agents to figure out resource collection, survival strategies, and cooperative/competitive behaviors from scratch in a dynamic world.

## 🚀 The Core Philosophy & Research Vision
While standard Reinforcement Learning (RL) algorithms perform exceptionally well in isolated environments, they often experience extreme instability and non-stationarity when multiple autonomous minds interact simultaneously. 

**Our primary objective is to expose and analyze the architectural limitations of pure mathematical Reinforcement Learning in replicating human-like decision-making.** 

This simulation proves that mathematical reward maximization alone is insufficient for complex multi-agent ecosystems. To bridge the gap between artificial execution and human cognitive traits, systems must model strategic hesitation, intentionality (Theory of Mind), and cognitive biases rather than relying solely on raw numerical optimization.

## 🔬 Core Research Areas
- **Multi-Agent Coordination:** Observing how agents interact, collaborate, or compete for limited resources.
- **Cognitive Complexity & Non-Stationarity:** Examining why standard DRL frameworks degrade or fluctuate as agent strategy co-evolves.
- **High-Speed Environment Modeling:** Designing a memory-contiguous simulation engine capable of microsecond state changes.
- **Theory of Mind Estimation:** Teaching agents to dynamically predict the intent and paths of competing entities.

## 💻 Tech Stack & Architecture
This repository implements a highly optimized, production-grade hybrid ecosystem:
- **Python & PyTorch** 🔥 (Deep Q-Networks & Cognitive Logic Processing)
- **Gymnasium** 🏋️‍♂️ (Custom Multi-Agent Environment Wrappers)
- **C++ Engine** ⚙️ (High-performance environment compilation linked via `pybind11` for maximum execution speed)
- **Go / Golang Gateway** 🐹 (Asynchronous, high-throughput network service for streaming and logging real-time agent telemetry)

## 📊 Live Telemetry & Simulation Dashboards
Below is the visual telemetry dashboard tracking non-stationary decision trajectories, phase portraits, system memory overhead, and cognitive friction during execution spikes:

<p align="center">
  <img src="assets/1_state_space_exploration.png" width="45%" alt="State Space Matrix" />
  <img src="assets/2_cognitive_friction_latency.png" width="45%" alt="Cognitive Friction" />
</p>

<p align="center">
  <img src="assets/3_strategy_drift.png" width="45%" alt="Strategy Drift" />
  <img src="assets/4_strategy_phase_portrait.png" width="45%" alt="Phase Portrait" />
</p>

<p align="center">
  <img src="assets/5_memory_overhead.png" width="45%" alt="Memory Matrix" />
  <img src="assets/6_pareto_frontier.png" width="45%" alt="Pareto Frontier" />
</p>

<p align="center">
  <img src="assets/7_telemetry_packet_loss.png" width="45%" alt="Packet Loss Analysis" />
  <img src="assets/8_policy_entropy_decay.png" width="45%" alt="Neural Policy Entropy" />
</p>

## 🚧 Current Status
* **Hybrid Core:** Completed! The Python training architecture, C++ physics layer, and Go telemetry gateway are fully integrated.
* **CI/CD Pipeline:** Automated integration testing via GitHub Actions is live (ensuring every commit maintains structural integrity).

---

### 🤝 Support & Follow
Are you fascinated by Artificial General Intelligence (AGI), Multi-Agent Systems, or the limitations of Deep RL in modeling cognitive behavior? 

**Please consider giving this repository a ⭐ STAR!** It helps the project grow and tracks our development journey!

Don't forget to **[Follow me on GitHub](https://github.com/Asmit-Singh-01)** to stay updated as we publish training logs, data graphs, and architectural updates. Let's push the boundaries of AI together! 🌍🤖
