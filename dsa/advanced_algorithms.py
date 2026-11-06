def greedy_priority_scheduling(orders):
    """
    Greedy algorithm for selecting orders.

    Orders with higher priority are processed first.
    If priority is equal, smaller order ID comes first.
    """

    remaining = orders.copy()

    result = []

    while remaining:

        best_index = 0

        for i in range(1, len(remaining)):

            current = remaining[i]
            best = remaining[best_index]

            current_priority = current.get("priority", 0)
            best_priority = best.get("priority", 0)

            if current_priority > best_priority:
                best_index = i

            elif (
                current_priority == best_priority
                and current["order_id"] < best["order_id"]
            ):
                best_index = i

        result.append(remaining.pop(best_index))

    return result


def optimize_printing_jobs(jobs, capacity):
    """
    Dynamic Programming - 0/1 Knapsack.

    Select printing jobs within a page capacity
    while maximizing total value.
    """

    n = len(jobs)

    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):

        pages = jobs[i - 1]["pages"]
        value = jobs[i - 1]["value"]

        for current_capacity in range(1, capacity + 1):

            if pages <= current_capacity:

                dp[i][current_capacity] = max(
                    dp[i - 1][current_capacity],

                    value + dp[
                        i - 1
                    ][current_capacity - pages]
                )

            else:

                dp[i][current_capacity] = dp[
                    i - 1
                ][current_capacity]

    selected_jobs = []

    current_capacity = capacity

    for i in range(n, 0, -1):

        if dp[i][current_capacity] != dp[i - 1][current_capacity]:

            job = jobs[i - 1]

            selected_jobs.append(job)

            current_capacity -= job["pages"]

    selected_jobs.reverse()

    return {
        "maximum_value": dp[n][capacity],
        "selected_jobs": selected_jobs
    }


def schedule_combinations(tasks, slots):
    """
    Backtracking algorithm.

    Generates possible schedules by assigning
    tasks to available slots.
    """

    results = []

    current_schedule = []

    used = set()

    def backtrack():

        if len(current_schedule) == slots:

            results.append(current_schedule.copy())
            return

        for task in tasks:

            if task not in used:

                used.add(task)
                current_schedule.append(task)

                backtrack()

                current_schedule.pop()
                used.remove(task)

    backtrack()

    return results


if __name__ == "__main__":

    print("===== ADVANCED ALGORITHMS =====")

    # -----------------------------
    # GREEDY
    # -----------------------------

    orders = [
        {
            "order_id": 101,
            "copies": 10,
            "priority": 2
        },
        {
            "order_id": 102,
            "copies": 5,
            "priority": 5
        },
        {
            "order_id": 103,
            "copies": 20,
            "priority": 3
        },
        {
            "order_id": 104,
            "copies": 8,
            "priority": 1
        }
    ]

    print("\nGreedy Priority Scheduling:")

    scheduled = greedy_priority_scheduling(orders)

    for order in scheduled:
        print(order)

    # -----------------------------
    # DYNAMIC PROGRAMMING
    # -----------------------------

    jobs = [
        {
            "job_id": "J1",
            "pages": 10,
            "value": 60
        },
        {
            "job_id": "J2",
            "pages": 20,
            "value": 100
        },
        {
            "job_id": "J3",
            "pages": 30,
            "value": 120
        }
    ]

    print("\nDynamic Programming:")

    result = optimize_printing_jobs(jobs, 50)

    print("Maximum Value:")
    print(result["maximum_value"])

    print("Selected Jobs:")
    print(result["selected_jobs"])

    # -----------------------------
    # BACKTRACKING
    # -----------------------------

    tasks = [
        "Print Order 1",
        "Print Order 2",
        "Print Order 3"
    ]

    print("\nBacktracking Schedules:")

    schedules = schedule_combinations(tasks, 2)

    for schedule in schedules:
        print(schedule)