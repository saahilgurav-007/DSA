"""
Stack, Queue & Monotonic Stack - Batch 2 (Problems 19, 20, 21, 23, 24, 26)
Each function: approach comment, time/space complexity, and a test case.
"""
 
from typing import List
 
 
# ---------------------------------------------------------------------------
# 19. Largest Rectangle in Histogram
# Approach: Monotonic increasing stack of indices. When a bar shorter than
# the stack top appears, pop and compute the rectangle with the popped bar
# as the height (width = distance between the new stack top and current
# index, minus 1). Sentinel 0 appended to flush remaining bars.
# O(n) time, O(n) space.
# ---------------------------------------------------------------------------
def largest_reactangle_histogram(heights: List[int]) -> int:
    stack = []
    max_area = 0
    heights = heights + [0]

    for i, h in enumerate(heights):
        while stack and heights[stack[-1]] > h:
            height = heights [stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)
    return max_area

# ---------------------------------------------------------------------------
# 20. Maximal Rectangle in Binary Matrix
# Approach: Reduce to "Largest Rectangle in Histogram" row by row. Maintain
# a running "height" array where height[j] = number of consecutive '1's
# ending at the current row in column j (resets to 0 on a '0'). Run the
# histogram algorithm on that height array for every row.
# O(rows * cols) time, O(cols) space.
# ---------------------------------------------------------------------------
def maximal_reactangle(matrix: List[List[str]]) -> int:
    if not matrix or not matrix[0]:
        return 0

    cols = len(matrix[0])
    heights = [0] * cols
    best = 0

    for row in matrix:
        for j in range(cols):
            heights[j] = heights[j] + 1 if row[j] == '1' else 0
        best = max(best, largest_reactangle_histogram(heights))

    return best

# ---------------------------------------------------------------------------
# 21. Sum of Subarray Minimums
# Approach: For each element, find how many subarrays it is the MINIMUM of.
# That count = (distance to previous strictly-smaller element) * (distance
# to next smaller-or-equal element). The strict/non-strict split avoids
# double-counting when duplicate values exist. Use two monotonic stacks
# (or one pass each direction). Sum contributions mod 1e9+7.
# O(n) time, O(n) space.
# ---------------------------------------------------------------------------
def sum_subarray_minimums(arr: List[int]) -> int:
    MOD = 10**9 + 7
    n = len(arr)
    left = [0] * n
    right = [0] * n

    stack = []
    for i in range(n):
        while stack and arr[stack[-1]] >= arr[i]:
            stack.pop()
        left[i] = i - (stack[-1] if stack else -1) 
        stack.append(i)

    stack = []
    for i in range(n - 1, -1, -1):
        while stack and arr[stack[-1]] > arr[i]:
            stack.pop()
        right[i] = (stack[-1] if stack else n) - i
        stack.append(i)

    total = 0
    for i in range(n):
        total = (total + arr[i] * left[i] * right[i]) % MOD

    return total

# ---------------------------------------------------------------------------
# 23. Remove K Digits for Smallest Number
# Approach: Greedy monotonic increasing stack. Scan digits left to right;
# while the last kept digit is bigger than the current one and we still
# have removals left, pop it (removing a bigger digit earlier always helps
# or is neutral). Strip leading zeros and leftover trailing removals.
# O(n) time, O(n) space.
# ---------------------------------------------------------------------------
def remove_k_digits(num: str, k: int) -> str:
    stack = []
    for digit in num:
        while stack and k > 0 and stack[-1] > digit:
            stack.pop()
            k -= 1
        stack.append(digit)
 
    if k > 0:            # still have removals left -> strip from the end
        stack = stack[:-k]
 
    result = ''.join(stack).lstrip('0')
    return result if result else "0"

# ---------------------------------------------------------------------------
# 24. Basic Calculator with Parentheses (+, -, and nested parentheses only)
# Approach: Single pass with a stack holding (sign_before_paren) context.
# Track current running result, current number being built, and current
# sign. On '(' push (result, sign) and reset; on ')' pop and combine.
# O(n) time, O(n) space (stack depth = nesting level).
# ---------------------------------------------------------------------------
def basic_calculator(s: str) -> int:
    stack = []
    result = 0
    number = 0
    sign = 1  # +1 or -1
 
    for ch in s:
        if ch.isdigit():
            number = number * 10 + int(ch)
        elif ch in '+-':
            result += sign * number
            number = 0
            sign = 1 if ch == '+' else -1
        elif ch == '(':
            stack.append(result)
            stack.append(sign)
            result = 0
            sign = 1
        elif ch == ')':
            result += sign * number
            number = 0
            prev_sign = stack.pop()
            prev_result = stack.pop()
            result = prev_result + prev_sign * result
        # spaces ignored
 
    result += sign * number
    return result
 
 
# ---------------------------------------------------------------------------
# 26. Asteroid Collision Simulation
# Approach: Stack simulation. Push right-moving (+) asteroids freely.
# A left-moving (-) asteroid collides with right-moving ones on top of the
# stack: smaller explodes, equal both explode, bigger survives and keeps
# colliding further down. O(n) time (amortized, each asteroid pushed/popped
# once), O(n) space.
# ---------------------------------------------------------------------------
def asteroid_collision(asteroids: List[int]) -> List[int]:
    stack = []
 
    for a in asteroids:
        alive = True
        while alive and a < 0 and stack and stack[-1] > 0:
            if stack[-1] < -a:
                stack.pop()      # top asteroid destroyed, keep checking
                continue
            elif stack[-1] == -a:
                stack.pop()      # both destroyed
            alive = False        # current asteroid destroyed (or mutual)
        if alive:
            stack.append(a)
 
    return stack
 
 
# ---------------------------------------------------------------------------
# Self-tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("19. Largest Rectangle Histogram:", largest_reactangle_histogram([2,1,5,6,2,3]))  
 
    matrix = [
        ["1","0","1","0","0"],
        ["1","0","1","1","1"],
        ["1","1","1","1","1"],
        ["1","0","0","1","0"],
    ]
    print("20. Maximal Rectangle:", maximal_reactangle(matrix)) 
 
    print("21. Sum of Subarray Minimums:", sum_subarray_minimums([3,1,2,4]))  
    print("23. Remove K Digits:", remove_k_digits("1432219", 3))              
    print("24. Basic Calculator:", basic_calculator("(1+(4+5+2)-3)+(6+8)"))   
    print("26. Asteroid Collision:", asteroid_collision([5,10,-5]))           
    print("26. Asteroid Collision:", asteroid_collision([8,-8]))             
    print("26. Asteroid Collision:", asteroid_collision([10,2,-5]))           
