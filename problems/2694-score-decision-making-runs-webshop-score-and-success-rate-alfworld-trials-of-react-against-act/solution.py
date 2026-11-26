
def webshop_metrics(episodes):
    if not episodes:
        return {"score": 0.0, "success_rate": 0.0}

    total_scores = 0
    successful_episodes = 0

    for episode in episodes:
        wanted = episode["wanted"]
        bought = episode["bought"]

        requirements = (
            len(wanted["attributes"])
            + len(wanted["options"])
            + (1 if wanted["max_price"] is not None else 0)
        )

        covered = 0

        if bought is not None:
            # Check wanted attributes
            for attr in wanted["attributes"]:
                if attr in bought["attributes"]:
                    covered += 1

            # Check wanted options
            for option in wanted["options"]:
                if option in bought["options"]:
                    covered += 1

            # Check price requirement
            max_price = wanted["max_price"]

            if max_price is not None:
                if bought["price"] < max_price:
                    covered += 1

        episode_score = covered / requirements
        total_scores += episode_score

        if covered == requirements:
            successful_episodes += 1

    score = (total_scores / len(episodes)) * 100
    success_rate = (successful_episodes / len(episodes)) * 100

    return {
        "score": round(score, 1),
        "success_rate": round(success_rate, 1)
    }


def alfworld_success(games):
    if not games:
        return {"All": 0.0}

    task_results = {}

    total_solved = 0

    for task_type, solved in games:
        if task_type not in task_results:
            task_results[task_type] = [0, 0]

        task_results[task_type][1] += 1

        if solved:
            task_results[task_type][0] += 1
            total_solved += 1

    result = {}

    for task_type, (solved, total) in task_results.items():
        rate = (solved / total) * 100
        result[task_type] = round(rate, 1)

    result["All"] = round((total_solved / len(games)) * 100, 1)

    return result


def compare_trials(react, act):
    react_sorted = sorted(react)
    act_sorted = sorted(act)

    react_avg = sum(react) / len(react)
    act_avg = sum(act) / len(act)

    relative_gains = [
        100 * (r - a) / a
        for r, a in zip(react, act)
    ]

    return {
        "react": {
            "best": round(max(react), 1),
            "avg": round(react_avg, 1),
            "worst": round(min(react), 1)
        },
        "act": {
            "best": round(max(act), 1),
            "avg": round(act_avg, 1),
            "worst": round(min(act), 1)
        },
        "relative_gain": {
            "min": round(min(relative_gains), 1),
            "max": round(max(relative_gains), 1),
            "avg": round(sum(relative_gains) / len(relative_gains), 1)
        },
        "react_wins_every_trial": all(
            r > a for r, a in zip(react, act)
        ),
        "worst_react_beats_best_act": min(react) > max(act)
    }
