from typing import List, Tuple

# ---------------------------------------------------------------------------
# 91. Job Sequencing with Deadlines
# ---------------------------------------------------------------------------
def job_sequencing(jobs: List[Tuple[str, int, int]]) -> Tuple[int, List[str]]:
    jobs_sorted = sorted(jobs, key=lambda j: j[2], reverse=True)
    max_deadline = max(j[1] for j in jobs) if jobs else 0
    slots = [None] * max_deadline
    total_profit = 0

    for job_id, deadline, profit in jobs_sorted:
        for t in range(min(deadline, max_deadline) -1, -1, -1):
            if slots[t] is None:
                slots[t] = job_id
                total_profit += profit
                break

    scheduled = [j for j in slots if j is not None]
    return total_profit, scheduled

# ---------------------------------------------------------------------------
# 92. Candy Distribution
# ---------------------------------------------------------------------------
def candy_distribution(ratings: List[int]) -> int:
    n = len(ratings)
    candies = [1] * n

    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            candies[i] = candies[i - 1] + 1

    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i + 1]:
            candies[i] = max(candies[i], candies[i + 1] + 1)

    return sum(candies)

# ---------------------------------------------------------------------------
# 93. Gas Station Circuit
# ---------------------------------------------------------------------------
def can_complete_circuit(gas: List[int], cost: List[int]) ->int:
    total_surplus = 0
    tank = 0
    start = 0

    for i in range(len(gas)):
        diff = gas[i] - cost[i]
        total_surplus += diff
        tank += diff
        if tank < 0:
            start = i + 1
            tank = 0

    return start if total_surplus >= 0 else -1

# ---------------------------------------------------------------------------
# 94. Minimum Number of Arrows to Burst Balloons
# ---------------------------------------------------------------------------
def min_arrows_to_burst_balloons(points: List[List[int]]) -> int:
    if not points:
        return 0

    points_sorted = sorted(points, key=lambda p: p[1])
    arrows = 1
    arrow_position = points_sorted[0][1]

    for start, end in points_sorted[1:]:
        if start > arrow_position:
            arrows += 1
            arrow_position = end

    return arrows

# ---------------------------------------------------------------------------
# 95. Jump Game II (minimum jumps to reach the last index)
# ---------------------------------------------------------------------------
def jump_game_ii(nums: List[int]) -> int:
    n = len(nums)
    if n <= 1:
        return 0

    jumps = 0
    current_end = 0
    farthest = 0

    for i in range(n - 1):
        farthest = max(farthest, i + nums[i])
        if i == current_end:
            jumps += 1
            current_end = farthest
            if current_end >= n - 1:
                break

    return jumps

# ---------------------------------------------------------------------------
# Self-tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    jobs91 = [("j1", 4, 20), ("j2", 1, 10), ("j3", 1, 40), ("j4", 1, 30)]
    profit, scheduled = job_sequencing(jobs91)
    print("91. Job Sequencing profit/scheduled:", profit, scheduled) 

    print("92. Candy Distribution [1,0,2]:", candy_distribution([1, 0, 2]))
    print("93. Gas Station start index:", can_complete_circuit([1,2,3,4,5], [3,4,5,1,2]))
    print("93. Gas Station (impossible):", can_complete_circuit([2,3,4], [3,4,3]))
    print("94. Min Arrows:", min_arrows_to_burst_balloons([[10,16],[2,8],[1,6],[7,12]]))
    print("95. Jump Game II [2,3,1,1,4]:", jump_game_ii([2, 3, 1, 1, 4]))
    print("95. Jump Game II [1,1,1,1]:", jump_game_ii([1, 1, 1, 1]))
     