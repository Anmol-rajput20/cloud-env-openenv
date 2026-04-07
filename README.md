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

## Observations

- Easy → both agents perform similarly  
- Medium → stochastic behavior affects outcomes  
- Hard → smart agent performs better  

This demonstrates that the environment is **non-trivial and realistic**

---

##  Key Insight

> The goal is not to hardcode intelligence, but to create an environment where intelligent behavior can emerge and be evaluated.

---

## Setup

```bash
pip install -r requirements.txt
python inference.py

