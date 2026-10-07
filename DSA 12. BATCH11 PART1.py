from typing import List
from collections import defaultdict
import bisect

# ---------------------------------------------------------------------------
# 103. Maximum XOR of Two Numbers in an Array
# ---------------------------------------------------------------------------
def find_maximum_xor(nums: List[int]) -> int:
    BITS = 31
    root = {}

    def insert(num):
        node = root
        for i in range(BITS, -1, -1):
            bit = (num >> i) & 1
            node = node.setdefault(bit, {})

    def query_max_xor(num):
        node = root
        result = 0
        for i in range(BITS, -1, -1):
            bit = (num >> i) & 1
            toggled = 1 - bit
            if toggled in node:
                result |= (1 << i)
                node = node[toggled]
            else:
                node = node[bit]
        return result

    for num in nums:
        insert(num)

    return max(query_max_xor(num) for num in nums)

# ---------------------------------------------------------------------------
# 109. Reverse Pairs (count i<j where nums[i] > 2*nums[j]) via Merge Sort
# ---------------------------------------------------------------------------
def reverse_pairs(nums: List[int]) -> int:
    def sort_count(arr):
        if len(arr) <= 1:
            return arr, 0
        mid = len(arr) // 2
        left, count_left = sort_count(arr[:mid])
        right, count_right = sort_count(arr[mid:])

        count_cross = 0
        j = 0
        for i in range(len(left)):
            while j < len(right) and left[i] > 2 * right[j]:
                j += 1
            count_cross += j

        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i]); i += 1
            else:
                merged.append(right[j]); j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])

        return merged, count_left + count_right + count_cross

    _, total = sort_count(nums)
    return total

# ---------------------------------------------------------------------------
# 118. Longest Consecutive Sequence (with Duplicates)
# ---------------------------------------------------------------------------
def longest_consecutive_sequence(nums: List[int]) -> int:
    num_set = set(nums)
    best = 0

    for num in num_set:
        if num - 1 in num_set:
            continue

        length = 1
        current = num
        while current + 1 in num_set:
            current += 1
            length += 1
        best = max(best, length)

    return best


# ---------------------------------------------------------------------------
# 122. Longest Repeating Character Replacement
# ---------------------------------------------------------------------------
def character_replacement(s: str, k: int) -> int:
    freq = defaultdict(int)
    left = 0
    max_freq = 0
    best = 0

    for right, ch in enumerate(s):
        freq[ch] += 1
        max_freq = max(max_freq, freq[ch])

        window_len = right - left + 1
        if window_len - max_freq > k:
            freq[s[left]] -= 1
            left += 1

        best = max(best, right - left + 1)

    return best

# ---------------------------------------------------------------------------
# 125. Count Subarrays with Product Less Than K
# ---------------------------------------------------------------------------
def count_subarrays_product_less_than_k(nums: List[int], k: int) -> int:
    if k <= 1:
        return 0  
 
    product = 1
    left = 0
    count = 0
 
    for right, x in enumerate(nums):
        product *= x
        while product >= k:
            product //= nums[left]
            left += 1
        count += right - left + 1
 
    return count
 
 
# ---------------------------------------------------------------------------
# 129. Sliding Window Median
# ---------------------------------------------------------------------------
def median_sliding_window(nums: List[int], k: int) -> List[float]:
    window = sorted(nums[:k])
    result = []
 
    def get_median(w):
        mid = len(w) // 2
        if len(w) % 2 == 1:
            return float(w[mid])
        return (w[mid - 1] + w[mid]) / 2.0
 
    result.append(get_median(window))
 
    for i in range(k, len(nums)):
        
        outgoing = nums[i - k]
        idx = bisect.bisect_left(window, outgoing)
        window.pop(idx)
        # insert the incoming element
        bisect.insort(window, nums[i])
        result.append(get_median(window))
 
    return result
 
 
# ---------------------------------------------------------------------------
# Self-tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("103. Max XOR:", find_maximum_xor([3, 10, 5, 25, 2, 8])) 
 
    print("109. Reverse Pairs [1,3,2,3,1]:", reverse_pairs([1, 3, 2, 3, 1]))  
    print("109. Reverse Pairs [2,4,3,5,1]:", reverse_pairs([2, 4, 3, 5, 1]))  
 
    print("118. Longest Consecutive (w/ dup):", longest_consecutive_sequence([100, 4, 200, 1, 3, 2, 2, 3]))  
 
    print("122. Char Replacement 'ABAB', k=2:", character_replacement("ABAB", 2))  
    print("122. Char Replacement 'AABABBA', k=1:", character_replacement("AABABBA", 1))  
 
    print("125. Subarrays Product<K, nums=[10,5,2,6], k=100:", count_subarrays_product_less_than_k([10,5,2,6], 100))  
 
    print("129. Sliding Window Median [1,3,-1,-3,5,3,6,7], k=3:", median_sliding_window([1,3,-1,-3,5,3,6,7], 3)) 