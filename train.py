import random
import matplotlib.pyplot as plt
from env import CloudEnv

# ---------------------------
# Simple Q-learning setup
# ---------------------------

ACTIONS = [0, 1, 2]

# Discretize CPU for table
def discretize_cpu(cpu):
    return int(cpu // 10)  # bucket (0–15)


# Q-table: (cpu_bucket, servers) -> action values
Q = {}

def get_q(state):
    key = (discretize_cpu(state.cpu), state.servers)
    if key not in Q:
        Q[key] = [0.0, 0.0, 0.0]
    return Q[key]


# Epsilon-greedy policy
def choose_action(state, epsilon=0.2):
    if random.random() < epsilon:
        return random.choice(ACTIONS)
    q_values = get_q(state)
    return q_values.index(max(q_values))


# ---------------------------
# Training Loop
# ---------------------------

def train(episodes=200):

    env = CloudEnv("medium")

    alpha = 0.1   # learning rate
    gamma = 0.9   # discount
    epsilon = 0.3

    rewards_per_episode = []

    for ep in range(episodes):

        state = env.reset()
        total_reward = 0

        while True:
            action = choose_action(state, epsilon)

            next_state, reward, done, _ = env.step(action)

            # Q-learning update
            q_values = get_q(state)
            next_q = get_q(next_state)

            q_values[action] = q_values[action] + alpha * (
                reward + gamma * max(next_q) - q_values[action]
            )

            state = next_state
            total_reward += reward

            if done:
                break

        rewards_per_episode.append(total_reward)

        # Decay epsilon
        epsilon = max(0.05, epsilon * 0.995)

        if (ep + 1) % 20 == 0:
            print(f"Episode {ep+1} | Reward: {total_reward:.2f}")

    return rewards_per_episode


# ---------------------------
# Plot + Save
# ---------------------------

def plot_rewards(rewards):
    import numpy as np

    plt.figure()

    window = 10
    smoothed = np.convolve(rewards, np.ones(window)/window, mode='valid')
    plt.plot(smoothed)
    plt.xlabel("Episode")
    plt.ylabel("Reward (smoothed)")
    plt.title("Training Reward Curve")

    plt.savefig("reward_curve.png")
    plt.show()


# ---------------------------
# Run
# ---------------------------

if __name__ == "__main__":
    rewards = train(episodes=200)
    plot_rewards(rewards)

import pickle

with open("q_table.pkl","wb") as f:
    pickle.dump(Q,f)

print("Q-table saved!")