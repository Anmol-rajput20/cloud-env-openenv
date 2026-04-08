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


def agent_policy(state):
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

    try:
        return int(response.choices[0].message.content.strip()[0])
    except:
        return 2  # fallback


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
        run_task(level)