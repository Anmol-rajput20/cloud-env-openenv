from env import CloudEnv
from grader import grade_episode
import random

# Reproducibility
random.seed(42)

# Simple rule-based agent
def agent_policy(state):
    capacity = state.servers * 50
    
    # if demand is higher than capacity -> add server
    if state.requests > capacity:
        return 0  # add server
    # if too many idle servers -> remove server
    elif state.requests < capacity * 0.5:
        return 1  # remove server
    else:
        return 2  # do nothing

def random_agent(state):
    return random.choice([0,1,2])

def run_episode(difficulty="easy",policy=agent_policy):
    env = CloudEnv(difficulty)
    state = env.reset()

    total_reward = 0

    while True:
        action = agent_policy(state)
        state, reward, done, _ = env.step(action)
        total_reward += reward

        if done:
            break

    return total_reward


def evaluate(difficulty):
    score = run_episode(difficulty)

    # Normalize score to 0 → 1
    normalized = max(0.0, min(1.0, (score + 50) / 100))
    return score, normalized


if __name__ == "__main__":
    for level in ["easy", "medium", "hard"]:
        smart = run_episode(level,agent_policy)
        random_score = run_episode(level,random_agent)

        smart_grade = grade_episode(smart)
        random_grade = grade_episode(random_score)


        print(f"\n {level.upper()} TASK")
        print(f"Smart Agent : {smart: .2f} -> Score: {smart_grade: .2f}")
        print(f"Random Agent: {random_score: .2f} -> Score: {random_grade: .2f}")