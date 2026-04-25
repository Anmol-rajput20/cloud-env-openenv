import random

# ---------------------------
# RULE-BASED AGENT (SMART)
# ---------------------------

def get_action(state):
    capacity = state.servers * 50

    if state.requests > capacity:
        return 0  # add server
    elif state.requests < capacity * 0.5:
        return 1  # remove server
    else:
        return 2  # do nothing


# ---------------------------
# RANDOM AGENT
# ---------------------------

def random_agent(state):
    return random.choice([0, 1, 2])