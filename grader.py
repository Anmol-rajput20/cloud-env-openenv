def grade_episode(total_reward):
    """
    Convert total reward into normalized score (0.0 t0 1.0)

    """

    score = (total_reward + 100) / 200

    score = max(0.0, min(1.0,score))

    return score