from typing import List, Tuple
import bisect

# ---------------------------------------------------------------------------
# 67. Longest Increasing Subsequence — O(n log n)
# ---------------------------------------------------------------------------
def longest_increasing_subsequence(nums: List[int]) -> int:
    tails = []
    for x in nums:
        pos = bisect.bisect_left(tails, x)
        if pos == len(tails):
            tails.append(x)
        else:
            tails[pos] = x
    return len(tails)

# ---------------------------------------------------------------------------
# 68. Longest Common Subsequence with Reconstruction
# ---------------------------------------------------------------------------
def longest_common_subsequence(text1: str, text2: str) -> Tuple[int, str]:
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    i, j = m, n
    chars = []
    while i > 0 and j > 0:
        if text1[i - 1] == text2[j - 1]:
            chars.append(text1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    return dp[m][n], ''.join(reversed(chars))

# ---------------------------------------------------------------------------
# 69. Edit Distance with Operation Reconstruction
# ---------------------------------------------------------------------------
def edit_distance_with_ops(word1: str, word2: str) -> Tuple[int, List[str]]:
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j - 1], dp[i - 1][j], dp[i][j - 1])

    ops = []
    i, j = m, n
    while i > 0 or j > 0:
        if i > 0 and j > 0 and word1[i - 1] == word2[j - 1]:
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
            ops.append(f"Replace '{word1[i-1]}' with '{word2[j-1]}' at position {i - 1}")
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            ops.append(f"Delete '{word1[i-1]}' at position {i-1}")
            i -= 1
        elif j > 0 and dp[i][j] == dp[i][j - 1] + 1:
            ops.append(f"Insert '{word2[j-1]}' at position {i}")   # BUG FIX: this branch was missing entirely
            j -= 1

    ops.reverse()
    return dp[m][n], ops

# ---------------------------------------------------------------------------
# 70. 0/1 Knapsack with Selected Items
# ---------------------------------------------------------------------------
def knapsack_01_with_items(weights: List[int], values: List[int], capacity: int) -> Tuple[int, List[int]]:
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(capacity + 1):
            dp[i][w] = dp[i - 1][w]
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i][w], values[i - 1] + dp[i - 1][w - weights[i - 1]])

    selected = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected.append(i - 1)
            w -= weights[i - 1]
    selected.reverse()

    return dp[n][capacity], selected

# ---------------------------------------------------------------------------
# 72. Coin Change II (count number of combinations to make amount)
# ---------------------------------------------------------------------------
def coin_change_combinations(amount: int, coins: List[int]) -> int:
    dp = [1] + [0] * amount
    for coin in coins:              # coin OUTER, amount INNER -> counts combinations not permutations
        for a in range(coin, amount + 1):
            dp[a] += dp[a - coin]
    return dp[amount]

# ---------------------------------------------------------------------------
# Self-tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("67. LIS length:", longest_increasing_subsequence([10, 9, 2, 5, 3, 7, 101, 18]))  # 4

    length, seq = longest_common_subsequence("abcde", "ace")
    print("68. LCS length/sequence:", length, seq)  # 3 ace

    dist, ops = edit_distance_with_ops("horse", "ros")
    print("69. Edit Distance:", dist)                # 3
    print("69. Operations:", ops)

    weights, values, capacity = [10, 20, 30], [60, 100, 120], 50
    best_value, items = knapsack_01_with_items(weights, values, capacity)
    print("70. Knapsack best value/items:", best_value, items)  # 220 [1, 2]

    print("72. Coin Change II ways:", coin_change_combinations(5, [1, 2, 5]))  # 4