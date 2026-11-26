import heapq

def analyze_ml_pipeline(tasks):

    if not tasks:
        return {
            "execution_order": [],
            "earliest_start": {},
            "earliest_finish": {},
            "latest_start": {},
            "latest_finish": {},
            "slack": {},
            "critical_path": [],
            "makespan": 0
        }

    # Step 1: Create task lookup dictionary
    task_map = {task["id"]: task for task in tasks}

    # Step 2: Build graph
    indegree = {task["id"]: 0 for task in tasks}
    successors = {task["id"]: [] for task in tasks}

    for task in tasks:
        task_id = task["id"]

        for dep in task["dependencies"]:
            successors[dep].append(task_id)
            indegree[task_id] += 1

    # Step 3: Topological sorting using min heap
    ready = []

    for task_id in indegree:
        if indegree[task_id] == 0:
            heapq.heappush(ready, task_id)

    execution_order = []

    earliest_start = {}
    earliest_finish = {}

    while ready:
        current = heapq.heappop(ready)

        execution_order.append(current)

        # Calculate earliest start
        start = 0

        for dep in task_map[current]["dependencies"]:
            start = max(start, earliest_finish[dep])

        finish = start + task_map[current]["duration"]

        earliest_start[current] = start
        earliest_finish[current] = finish

        # Update successors
        for next_task in successors[current]:
            indegree[next_task] -= 1

            if indegree[next_task] == 0:
                heapq.heappush(ready, next_task)

    # Step 4: Calculate makespan
    makespan = max(earliest_finish.values())

    # Step 5: Backward pass
    latest_start = {}
    latest_finish = {}
    slack = {}

    for current in reversed(execution_order):

        if successors[current]:
            finish = min(
                latest_start[successor]
                for successor in successors[current]
            )
        else:
            finish = makespan

        start = finish - task_map[current]["duration"]

        latest_finish[current] = finish
        latest_start[current] = start

        slack[current] = start - earliest_start[current]

    # Step 6: Arrange dictionaries in execution order
    latest_start = {
        task: latest_start[task] for task in execution_order
    }

    latest_finish = {
        task: latest_finish[task] for task in execution_order
    }

    slack = {
        task: slack[task] for task in execution_order
    }

    # Step 7: Find critical path
    critical_path = [
        task for task in execution_order
        if slack[task] == 0
    ]

    return {
        "execution_order": execution_order,
        "earliest_start": earliest_start,
        "earliest_finish": earliest_finish,
        "latest_start": latest_start,
        "latest_finish": latest_finish,
        "slack": slack,
        "critical_path": critical_path,
        "makespan": makespan
    }
