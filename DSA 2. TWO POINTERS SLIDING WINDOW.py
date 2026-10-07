"""
Two Pointers & Sliding Window - Batch 1 (Problems 11-18, core 6)
Each function: approach comment, time/space complexity, and a test case.
"""
 
from typing import List
from collections import deque, defaultdict, Counter
 
 
# ---------------------------------------------------------------------------
# 11. Minimum Window Substring
# Approach: Sliding window with a "need" counter (chars required from t) and
# a "have" counter (matched chars in current window). Expand right until the
# window is valid, then shrink left while still valid, tracking the best
# window seen. O(n + m) time, O(k) space (k = distinct chars in t).
# ---------------------------------------------------------------------------
def min_window_substring(s: str, t: str) -> str:
    if not s or not t:
        return ""

    need = Counter(t)
    missing = len(t)  # total chars still needed (with multiplicity)
    left = 0
    best_len = float('inf')
    best_start = 0
 
    for right, ch in enumerate(s):
        if need[ch] > 0:
            missing -= 1
        need[ch] -= 1
 
        while missing == 0:
            if right - left + 1 < best_len:
                best_len = right - left + 1
                best_start = left
            need[s[left]] += 1
            if need[s[left]] > 0:
                missing += 1
            left += 1
 
    return "" if best_len == float('inf') else s[best_start:best_start + best_len]

# ---------------------------------------------------------------------------
# 12. Sliding Window Maximum
# Approach: Monotonic decreasing deque storing indices. Front of deque is
# always the max of the current window. Pop from back while smaller than
# incoming element; pop from front if it fell out of the window.
# O(n) time (each index pushed/popped once), O(k) space.
# ---------------------------------------------------------------------------
def sliding_window_maximum(nums: List[int], k: int) -> List[int]:
    dq = deque()
    result = []

    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)

        if dq[0] <= i - k:
            dq.popleft()

        if i >= k - 1:
            result.append(nums[dq[0]])

    return result

# ---------------------------------------------------------------------------
# 13. Longest Substring with At Most K Distinct Characters
# Approach: Sliding window with a frequency map. Expand right always; when
# distinct count exceeds k, shrink left until it's back to <= k.
# O(n) time, O(k) space.
# ---------------------------------------------------------------------------
def longest_substring_at_most_k_distinct(s: str, k: int) -> int:
    if k == 0:
        return 0
 
    freq = defaultdict(int)
    left = 0
    best = 0
 
    for right, ch in enumerate(s):
        freq[ch] += 1
        while len(freq) > k:
            left_ch = s[left]
            freq[left_ch] -= 1
            if freq[left_ch] == 0:
                del freq[left_ch]
            left += 1
        best = max(best, right - left + 1)
 
    return best
 
 
# ---------------------------------------------------------------------------
# 14. Subarrays with K Different Integers
# Approach: Exact(K) = AtMost(K) - AtMost(K-1). AtMost(k) counts subarrays
# with at most k distinct integers via sliding window; for a fixed right,
# every left in [window_left, right] gives a valid subarray, contributing
# (right - window_left + 1) subarrays. O(n) time, O(n) space.
# ---------------------------------------------------------------------------
def subarrays_with_k_distinct(nums: List[int], k: int) -> int:
    def at_most(k: int) -> int:
        if k < 0:
            return 0
        freq = defaultdict(int)
        left = 0
        count = 0
        for right, x in enumerate(nums):
            freq[x] += 1
            while len(freq) > k:
                freq[nums[left]] -= 1
                if freq[nums[left]] == 0:
                    del freq[nums[left]]
                left += 1
            count += right - left + 1
        return count
 
    return at_most(k) - at_most(k - 1)
 
 
# ---------------------------------------------------------------------------
# 15. Minimum Size Subarray Sum with Negative Numbers
# Approach: Plain two-pointer FAILS here because prefix sums aren't
# monotonic once negatives are allowed (shrinking the window can increase
# the sum). Correct approach: prefix sums + monotonic increasing deque of
# indices (this is LeetCode 862's technique). For each right index j, pop
# from the front while prefix[j] - prefix[front] >= target (record the
# length), then maintain deque increasing by popping any back index whose
# prefix >= prefix[j] (it can never beat j as a left boundary again).
# O(n) time, O(n) space.
# ---------------------------------------------------------------------------
def min_size_subarray_sum_with_negatives(nums: List[int], target: int) -> int:
    n = len(nums)
    prefix = [0] * (n + 1)
    for i, x in enumerate(nums):
        prefix[i + 1] = prefix[i] + x
 
    dq = deque() 
    best = float('inf')
 
    for j in range(n + 1):
        while dq and prefix[j] - prefix[dq[0]] >= target:
            best = min(best, j - dq.popleft())
        while dq and prefix[dq[-1]] >= prefix[j]:
            dq.pop()
        dq.append(j)
 
    return best if best != float('inf') else -1
 
 
# ---------------------------------------------------------------------------
# 16 (list #18). Maximum Points from Cards
# Approach: Taking k cards from either end = leaving a contiguous block of
# (n-k) cards untaken in the middle. Maximize total = minimize the sum of
# that untouched middle window of size (n-k), via a plain fixed-size
# sliding window. Answer = total_sum - min_window_sum. O(n) time, O(1) space.
# ---------------------------------------------------------------------------
def max_points_from_cards(card_points: List[int], k: int) -> int:
    n = len(card_points)
    window_size = n - k
    total = sum(card_points)
 
    if window_size == 0:
        return total  # take all cards
 
    window_sum = sum(card_points[:window_size])
    min_window = window_sum
 
    for i in range(window_size, n):
        window_sum += card_points[i] - card_points[i - window_size]
        min_window = min(min_window, window_sum)
 
    return total - min_window
 
 
# ---------------------------------------------------------------------------
# Self-tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("11. Min Window Substring:", min_window_substring("ADOBECODEBANC", "ABC")) 
    print("12. Sliding Window Max:", sliding_window_maximum([1,3,-1,-3,5,3,6,7], 3))    
    print("13. Longest Substr At Most K Distinct:", longest_substring_at_most_k_distinct("eceba", 2))  
    print("14. Subarrays w/ K Distinct:", subarrays_with_k_distinct([1,2,1,2,3], 2))     
    print("15. Min Size Subarray (neg allowed):", min_size_subarray_sum_with_negatives([2,-1,2], 3))   
    print("18. Max Points From Cards:", max_points_from_cards([1,79,80,1,1,1,200,1], 3))  