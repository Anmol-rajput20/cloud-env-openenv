---
title: Cloud Env Openenv
emoji: 📉
colorFrom: gray
colorTo: indigo
sdk: docker
pinned: false
license: mit
short_description: Openenv cloud resource optimization environment
---

## 🔗 Live Demo

Hugging Face Space:  
https://huggingface.co/spaces/anmol1620/cloud-env-openenv

# Cloud Resource Management Environment (OpenEnv)

## Overview

This project simulates a real-world cloud resource management system, where an AI agent dynamically scales server infrastructure based on incoming traffic.

Inspired by real-world systems like Amazon Web Services, the environment models:

- Dynamic traffic patterns  
- Server failures  
- Delayed scaling (realistic provisioning)  
- Cost vs performance trade-offs  

---

##  Objective

Design an agent that:

- Maintains optimal CPU utilization  
- Minimizes infrastructure cost  
- Adapts to unpredictable demand  

---

##  Environment Design

###  State (Observation Space)

- `cpu` → current CPU utilization (%)  
- `servers` → number of active servers  
- `requests` → incoming traffic  
- `cost` → infrastructure cost  

---

###  Actions (Action Space)

- `0` → Add server  
- `1` → Remove server  
- `2` → Do nothing  

---

## OpenEnv API

- `reset()` → initializes environment  
- `step(action)` → returns (state, reward, done, info)  
- `state()` → returns current state  

---

## Reward Function

The reward is designed to reflect real-world trade-offs:

- High reward for optimal CPU usage  
- Penalty for overloading (CPU > 100%)  
- Penalty for high infrastructure cost  
- Penalty for unstable scaling  

This provides **continuous learning signals**, not just final success/failure.

---

## Tasks

| Task | Description |
|------|------------|
| Easy | Stable and predictable traffic |
| Medium | Moderate fluctuations |
| Hard | High volatility + sudden spikes |

---

## Grading System

Each episode is evaluated using a normalized score:

- `0.0` → poor performance  
- `1.0` → optimal behavior  

---

## Baseline Agents

### Smart Agent
Rule-based policy using:
- CPU thresholds  
- demand vs capacity  

### Random Agent
Random action selection

---

## 📊 Results

### Agent Performance Comparison

| Agent        | Score |
|-------------|------|
| Random       | -4.46 |
| Rule-Based   | 3.98 |
| Trained RL   | 71.42 |

👉 The trained RL agent significantly outperforms both random and rule-based agents, demonstrating successful learning and adaptation.

### 📈 Training Reward Curve

![Reward Curve](reward_curve.png)

## Observations

- Easy → both agents perform similarly  
- Medium → stochastic behavior affects outcomes  
- Hard → smart agent performs better  

This demonstrates that the environment is **non-trivial and realistic**

---

## 💡 Key Insight

The RL-trained agent learns to dynamically balance:
- Performance (CPU utilization)
- Cost (number of servers)
- Stability (smooth scaling)

Unlike static rule-based systems, it adapts to changing demand and achieves significantly higher rewards.
---

## 🔗 Important Links

- 🌐 Hugging Face Space: https://huggingface.co/spaces/anmol1620/cloud-env-openenv
- 📓 Colab Notebook: [Add Link]
- 🎥 Demo Video / Blog: [Add Link]
- 💻 GitHub Repo: https://github.com/Anmol-rajput20/cloud-env-openenv

## Setup

```bash
pip install -r requirements.txt
python inference.py

