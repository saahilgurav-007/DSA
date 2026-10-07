from typing import List
# ---------------------------------------------------------------------------
# 83. Partition Array for Maximum Sum
# ---------------------------------------------------------------------------
def max_sum_after_partitioning(arr: List[int], k: int) -> int:
    n = len(arr)
    dp = [0] * (n + 1)

    for i in range(1, n + 1):
        current_max = 0
        for L in range(1, min(k, i) + 1):
            current_max = max(current_max, arr[i - L])
            dp[i] = max(dp[i], dp[i - L] + current_max * L)

    return dp[n]

# ---------------------------------------------------------------------------
# 84. Maximum Profit with K Stock Transactions
# ---------------------------------------------------------------------------
def max_profit_k_transactions(k: int, prices: List[int]) -> int:
    n = len(prices)
    if n == 0 or k == 0:
        return 0

    if k >= n // 2:
        return sum(max(0, prices[i] - prices[i - 1]) for i in range(1, n))

    hold = [float('-inf')] * (k + 1)
    sold = [0] * (k + 1)

    for price in prices:
        for t in range(1, k + 1):
            hold[t] = max(hold[t], sold[t - 1] - price)
            sold[t] = max(sold[t], hold[t] + price)
    return sold[k]

# ---------------------------------------------------------------------------
# Self-tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("83. Max Sum After Partitioning:", max_sum_after_partitioning([1, 15, 7, 9, 2, 5, 10], 3))  
 
    print("84. Max Profit k=2:", max_profit_k_transactions(2, [3, 2, 6, 5, 0, 3]))  
    print("84. Max Profit k=2, trending up:", max_profit_k_transactions(2, [1, 2, 3, 4, 5]))  
    print("84. Max Profit k=0:", max_profit_k_transactions(0, [1, 2, 3]))  
    print("84. Max Profit large k (unlimited-equivalent):", max_profit_k_transactions(100, [3, 2, 6, 5, 0, 3]))  