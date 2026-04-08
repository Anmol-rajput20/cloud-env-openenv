from env import CloudEnv
from openai import OpenAI
import os
import random

client = OpenAI(
    base_url=os.environ.get("API_BASE_URL", "https://api.openai.com/v1"),
    api_key=os.environ.get("API_KEY", "dummy-key")
)

MODEL = os.environ.get("MODEL_NAME","gpt-4o-mini")

random.seed(42)

def fallback_policy(state):
    if state.cpu > 75:
        return 0  # add server
    elif state.cpu < 40:
        return 1  # remove server
    else:
        return 2  # do nothing

def agent_policy(state):
    try:
        # If API not available → fallback
        if "API_KEY" not in os.environ:
            return fallback_policy(state)

        prompt = f"""
You are managing cloud servers.

State:
CPU: {state.cpu}
Servers: {state.servers}
Requests: {state.requests}

Actions:
0 = Add server
1 = Remove server
2 = Do nothing

Return only the number (0, 1, or 2).
"""

        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        text = response.choices[0].message.content.strip()

        
        for char in text:
            if char in ["0", "1", "2"]:
                return int(char)

        return fallback_policy(state)

    except Exception:
        return fallback_policy(state)



def run_task(difficulty):
    env = CloudEnv(difficulty)
    state = env.reset()

    print(f"[START] difficulty={difficulty}")

    total_reward = 0
    step = 0

    while True:
        step += 1
        action = agent_policy(state)
        state, reward, done, _ = env.step(action)

        total_reward += reward

        print(f"[STEP] step={step} cpu={state.cpu:.2f} servers={state.servers} requests={state.requests} reward={reward:.2f}")

        if done:
            break

    score = max(0.0, min(1.0, (total_reward + 50) / 100))

    print(f"[END] difficulty={difficulty} total_reward={total_reward:.2f} score={score:.2f}")


if __name__ == "__main__":
    for level in ["easy", "medium", "hard"]:
        try:
            run_task(level)
        except Exception:
            print(f"[END] difficulty={level} total_reward=0 score=0.0")