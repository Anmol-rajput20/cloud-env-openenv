import pickle
from env import CloudEnv

# Load trained Q-table
with open("q_table.pkl", "rb") as f:
    Q = pickle.load(f)

def discretize_cpu(cpu):
    return int(cpu // 10)

def get_action(state):
    key = (discretize_cpu(state.cpu), state.servers)

    if key not in Q:
        return 2  # default = do nothing

    return Q[key].index(max(Q[key]))


# Test run
if __name__ == "__main__":
    env = CloudEnv("medium")
    state = env.reset()

    total_reward = 0

    while True:
        action = get_action(state)
        state, reward, done, _ = env.step(action)
        total_reward += reward

        if done:
            break

    print("Total Reward:", total_reward)