import random
from env import CloudEnv
from agent import get_action  # your LLM agent


# ---------------------------
# BASELINE AGENTS
# ---------------------------

def random_agent(state):
    return random.choice([0, 1, 2])


def rule_based_agent(state):
    if state.cpu > 80:
        return 0  # add server
    elif state.cpu < 40:
        return 1  # remove server
    else:
        return 2  # do nothing


# ---------------------------
# RUN EPISODE
# ---------------------------

def run_episode(env, agent_fn):
    state = env.reset()

    history = []

    done = False

    while not done:
        action = agent_fn(state)

        next_state, reward, done, _ = env.step(action)

        history.append({
            "cpu": next_state.cpu,
            "servers": next_state.servers,
            "cost": next_state.cost,
            "reward": reward
        })

        state = next_state

    return history


# ---------------------------
# VERIFIER (CORE LOGIC)
# ---------------------------

def evaluate_episode(history):
    total_reward = sum(h["reward"] for h in history)

    avg_cpu = sum(h["cpu"] for h in history) / len(history)
    avg_cost = sum(h["cost"] for h in history) / len(history)

    overloads = sum(1 for h in history if h["cpu"] > 100)
    optimal_cpu = sum(1 for h in history if 50 <= h["cpu"] <= 75)

    # FINAL SCORE (you can tweak this)
    score = (
        total_reward
        + optimal_cpu * 2
        - overloads * 3
        - avg_cost * 0.1
    )

    return {
        "score": score,
        "total_reward": total_reward,
        "avg_cpu": avg_cpu,
        "avg_cost": avg_cost,
        "overloads": overloads,
        "optimal_steps": optimal_cpu
    }


# ---------------------------
# TEST ALL AGENTS
# ---------------------------

def evaluate_agent(agent_fn, name):
    env = CloudEnv("medium")

    history = run_episode(env, agent_fn)
    result = evaluate_episode(history)

    print(f"\n=== {name} ===")
    for k, v in result.items():
        print(f"{k}: {round(v, 2)}")


# ---------------------------
# MAIN
# ---------------------------

if __name__ == "__main__":

    evaluate_agent(random_agent, "Random Agent")
    evaluate_agent(rule_based_agent, "Rule-Based Agent")

    # LLM agent wrapper
    def llm_agent(state):
        return get_action(state)

    evaluate_agent(llm_agent, "LLM Agent")