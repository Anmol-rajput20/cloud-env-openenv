from agent import get_action as rule_agent
from trained_agent import get_action as trained_agent
from env import CloudEnv
import random

def random_agent(state):
    return random.choice([0,1,2])

def run_episode(policy):
    env = CloudEnv("medium")
    state = env.reset()
    total_reward = 0

    while True:
        action = policy(state)
        state, reward, done, _ = env.step(action)
        total_reward += reward

        if done:
            break

    return total_reward


if __name__ == "__main__":

    print("\n=== Comparison ===")

    r1 = run_episode(random_agent)
    r2 = run_episode(rule_agent)
    r3 = run_episode(trained_agent)

    print(f"Random Agent  : {r1:.2f}")
    print(f"Rule Agent    : {r2:.2f}")
    print(f"Trained Agent : {r3:.2f}")