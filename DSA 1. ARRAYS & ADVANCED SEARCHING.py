from typing import List, Tuple
import heapq

# ---------------------------------------------------------------------------
# 1. Median of Two Sorted Arrays
# ---------------------------------------------------------------------------
def median_two_sorted_arrays(nums1: List[int], nums2: List[int]) -> float:
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
    m, n = len(nums1), len(nums2)
    lo, hi = 0, m
    half = (m + n + 1) // 2

    while lo <= hi:
        i = (lo + hi) // 2
        j = half - i

        left1 = nums1[i - 1] if i > 0 else float('-inf')
        right1 = nums1[i] if i < m else float('inf')
        left2 = nums2[j - 1] if j > 0 else float('-inf')
        right2 = nums2[j] if j < n else float('inf')

        if left1 <= right2 and left2 <= right1:
            if (m + n) % 2 == 1:
                return max(left1, left2)
            return (max(left1, left2) + min(right1, right2)) / 2.0
        elif left1 > right2:
            hi = i - 1
        else:
            lo = i + 1
    raise ValueError("Input arrays not sorted / invalid")

# ---------------------------------------------------------------------------
# 2. First Missing Positive
# ---------------------------------------------------------------------------
def first_missing_positive(nums: List[int]) -> int:
    n = len(nums)
    for i in range(n):
        while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
            correct = nums[i] - 1
            nums[i], nums[correct] = nums[correct], nums[i]
    for i in range(n):
        if nums[i] != i + 1:
            return i + 1
    return n + 1

# ---------------------------------------------------------------------------
# 3. Trapping Rain Water       
# ---------------------------------------------------------------------------
def trap_rain_water(height: List[int]) -> int:
    if not height:
        return 0
    left, right = 0, len(height) - 1
    left_max, right_max = height[left], height[right]
    water = 0
    while left < right:
        if left_max <= right_max:
            left += 1
            left_max = max(left_max, height[left])
            water += left_max - height[left]
        else:
            right -= 1
            right_max = max(right_max, height[right])
            water += right_max - height[right]
    return water

# ---------------------------------------------------------------------------
# 4. Maximum Sum Circular Subarray
# ---------------------------------------------------------------------------
def max_subarray_sum_circular(nums: List[int]) -> int:
    total = 0
    cur_max, max_sum = 0, nums[0]
    cur_min, min_sum = 0, nums[0]

    for x in nums:
        cur_max = max(cur_max, 0) + x
        max_sum = max(max_sum, cur_max)
        cur_min = min(cur_min, 0) + x
        min_sum = min(min_sum, cur_min)

        total += x

    if max_sum < 0:
        return max_sum
    return max(max_sum, total - min_sum)

# ---------------------------------------------------------------------------
# 5. Count Inversions in an Array  
# ---------------------------------------------------------------------------
def count_inversions(arr: List[int]) -> int:
    def sort_count(a: List[int]) -> Tuple[List[int], int]:
        if len(a) <= 1:
            return a, 0
        mid = len(a) // 2
        left, inv_left = sort_count(a[:mid])
        right, inv_right = sort_count(a[mid:])
 
        merged = []
        i = j = inv_cross = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
                inv_cross += len(left) - i  
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged, inv_left + inv_right + inv_cross
 
    _, total = sort_count(arr)
    return total
 
 
# ---------------------------------------------------------------------------
# 6. Maximum Product Subarray
# ---------------------------------------------------------------------------
def max_product_subarray(nums: List[int]) -> int:
    result = nums[0]
    cur_max = cur_min = nums[0]
 
    for x in nums[1:]:
        candidates = (x, cur_max * x, cur_min * x)
        cur_max = max(candidates)
        cur_min = min(candidates)
        result = max(result, cur_max)
 
    return result
 
 
# ---------------------------------------------------------------------------
# 7. Largest Sum Contiguous Subarray with Indices
# ---------------------------------------------------------------------------
def max_subarray_with_indices(nums: List[int]) -> Tuple[int, int, int]:
    
    max_sum = cur_sum = nums[0]
    start = end = 0
    temp_start = 0
 
    for i in range(1, len(nums)):
        if nums[i] > cur_sum + nums[i]:
            cur_sum = nums[i]
            temp_start = i
        else:
            cur_sum += nums[i]
 
        if cur_sum > max_sum:
            max_sum = cur_sum
            start = temp_start
            end = i
 
    return max_sum, start, end  
 
 
# ---------------------------------------------------------------------------
# 8. Find Duplicate Number (Floyd's Cycle Detection)
# ---------------------------------------------------------------------------
def find_duplicate(nums: List[int]) -> int:
    slow = fast = nums[0]
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
 
    slow2 = nums[0]
    while slow2 != slow:
        slow2 = nums[slow2]
        slow = nums[slow]
 
    return slow
 
 
# ---------------------------------------------------------------------------
# 9. Split Array Largest Sum
# ---------------------------------------------------------------------------
def split_array_largest_sum(nums: List[int], k: int) -> int:
    def pieces_needed(max_sum: int) -> int:
        pieces, cur = 1, 0
        for x in nums:
            if cur + x > max_sum:
                pieces += 1
                cur = x
            else:
                cur += x
        return pieces
 
    lo, hi = max(nums), sum(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if pieces_needed(mid) <= k:
            hi = mid         
        else:
            lo = mid + 1      
    return lo
 
 
# ---------------------------------------------------------------------------
# 10. Kth Smallest Element in a Sorted Matrix
# ---------------------------------------------------------------------------
def kth_smallest_in_matrix(matrix: List[List[int]], k: int) -> int:
    n = len(matrix)
 
    def count_less_equal(x: int) -> int:
        count = 0
        row, col = n - 1, 0
        while row >= 0 and col < n:
            if matrix[row][col] <= x:
                count += row + 1
                col += 1
            else:
                row -= 1
        return count
 
    lo, hi = matrix[0][0], matrix[n - 1][n - 1]
    while lo < hi:
        mid = (lo + hi) // 2
        if count_less_equal(mid) < k:
            lo = mid + 1
        else:
            hi = mid
    return lo
 
 
# ---------------------------------------------------------------------------
# Self-tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("1. Median:", median_two_sorted_arrays([1, 3], [2]))                      
    print("2. First Missing Positive:", first_missing_positive([3, 4, -1, 1]))       
    print("3. Trap Rain Water:", trap_rain_water([0,1,0,2,1,0,1,3,2,1,2,1]))         
    print("4. Max Circular Subarray:", max_subarray_sum_circular([5,-3,5]))          
    print("5. Count Inversions:", count_inversions([8, 4, 2, 1]))                    
    print("6. Max Product Subarray:", max_product_subarray([2,3,-2,4]))              
    print("7. Max Subarray w/ Indices:", max_subarray_with_indices([-2,1,-3,4,-1,2,1,-5,4]))  
    print("8. Find Duplicate:", find_duplicate([1,3,4,2,2]))                          
    print("9. Split Array Largest Sum:", split_array_largest_sum([7,2,5,10,8], 2))    
    print("10. Kth Smallest in Matrix:", kth_smallest_in_matrix([[1,5,9],[10,11,13],[12,13,15]], 8))  
