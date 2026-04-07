import os
import random
from env import CloudEnv
from grader import grade_episode

# Required environment variables
API_BASE_URL = os.getenv("API_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")
HF_TOKEN = os.getenv("HF_TOKEN")

random.seed(42)


# Smart agent
def agent_policy(state):
    capacity = state.servers * 50

    if state.cpu > 90:
        return 0
    elif state.cpu < 30:
        return 1
    elif state.requests > capacity * 0.85:
        return 0
    elif state.requests < capacity * 0.6:
        return 1
    else:
        return 2


# Run one episode
def run_episode(difficulty):
    env = CloudEnv(difficulty)
    state = env.reset()

    total_reward = 0
    step_count = 0

    print(f"[START] difficulty={difficulty}")

    while True:
        action = agent_policy(state)
        state, reward, done, _ = env.step(action)

        total_reward += reward
        step_count += 1

        print(f"[STEP] step={step_count} cpu={state.cpu:.2f} servers={state.servers} requests={state.requests} reward={reward:.2f}")

        if done:
            break

    score = grade_episode(total_reward)

    print(f"[END] difficulty={difficulty} total_reward={total_reward:.2f} score={score:.2f}")

    return score


# 🔹 Run all tasks
if __name__ == "__main__":
    for level in ["easy", "medium", "hard"]:
        run_episode(level)