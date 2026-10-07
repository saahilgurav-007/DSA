from typing import List
import heapq
from collections import Counter, deque

# ---------------------------------------------------------------------------
# 45. Find Median from Data Stream
# ---------------------------------------------------------------------------
class MedianFinder:
    def __init__(self):
        self.low = []
        self.high = []

    def add_num(self, num: int) -> None:
        heapq.heappush(self.low, -num)
        heapq.heappush(self.high, -heapq.heappop(self.low))

        if len(self.high) > len(self.low):
            heapq.heappush(self.low, -heapq.heappop(self.high))

    def find_median(self) -> float:
        if len(self.low) > len(self.high):
            return float(-self.low[0])
        return (-self.low[0] + self.high[0]) / 2.0

# ---------------------------------------------------------------------------
# 48. Kth Largest Element in a Stream
# ---------------------------------------------------------------------------
class KthLargest:
    def __init__(self, k: int, nums: List[int]):
        self.k = k
        self.heap = nums[:]
        heapq.heapify(self.heap)
        while len(self.heap) > k:
            heapq.heappop(self.heap)

    def add(self, val: int) -> int:
        heapq.heappush(self.heap, val)
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)
        return self.heap[0]

# ---------------------------------------------------------------------------
# 49. Smallest Range Covering Elements from K Lists
# ---------------------------------------------------------------------------
def smallest_range_k_lists(lists: List[List[int]]) -> List[int]:
    heap = []
    current_max = float('-inf')
    for i, lst in enumerate(lists):
        heapq.heappush(heap, (lst[0], i, 0))
        current_max = max(current_max, lst[0])

    best_range = None
    while True:
        val, list_i, elem_i = heapq.heappop(heap)
        if best_range is None or current_max - val < best_range[1] - best_range[0]:
            best_range = [val, current_max]
        if elem_i + 1 == len(lists[list_i]):
            break
        next_val = lists[list_i][elem_i + 1]
        current_max = max(current_max, next_val)
        heapq.heappush(heap, (next_val, list_i, elem_i + 1))
    return best_range

# ---------------------------------------------------------------------------
# 50. Reorganize String
#---------------------------------------------------------------------------
def reorganize_string(s: str) -> str:
    count = Counter(s)
    heap = [(-c, ch) for ch, c in count.items()]
    heapq.heapify(heap)

    result = []
    prev = None

    while heap or prev:
        if not heap:
            return ""  
 
        cnt, ch = heapq.heappop(heap)
        result.append(ch)
        cnt += 1  
 
        if prev:
            heapq.heappush(heap, prev)
            prev = None
        if cnt < 0:  
            prev = (cnt, ch)
 
    return ''.join(result) if len(result) == len(s) else ""
 
# ---------------------------------------------------------------------------
# 51. Task Scheduler with Cooldown Periods
# ---------------------------------------------------------------------------
def least_interval(tasks: List[str], n: int) -> int:
    counts = Counter(tasks)
    max_count = max(counts.values())
    num_at_max = sum(1 for c in counts.values() if c == max_count)
    return max(len(tasks), (max_count - 1) * (n + 1) + num_at_max)
 
 
def least_interval_simulation(tasks: List[str], n: int) -> int:
    """Cross-check via explicit heap + cooldown-queue simulation (slower,
    used only to verify the closed-form formula above agrees on random
    inputs)."""
    counts = Counter(tasks)
    heap = [-c for c in counts.values()]
    heapq.heapify(heap)
    time = 0
    cooldown = deque()  
 
    while heap or cooldown:
        time += 1
        if heap:
            cnt = heapq.heappop(heap) + 1  
            if cnt < 0:
                cooldown.append((time + n, cnt))
        if cooldown and cooldown[0][0] == time:
            _, cnt = cooldown.popleft()
            heapq.heappush(heap, cnt)
 
    return time
 
 
# ---------------------------------------------------------------------------
# Self-tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    mf = MedianFinder()
    for x in [5, 15, 1, 3]:
        mf.add_num(x)
    print("45. Median after [5,15,1,3]:", mf.find_median()) 
 
    kl = KthLargest(3, [4, 5, 8, 2])
    print("48. KthLargest.add(3):", kl.add(3))   
    print("48. KthLargest.add(5):", kl.add(5)) 
    print("48. KthLargest.add(10):", kl.add(10)) 
    print("48. KthLargest.add(9):", kl.add(9))  
 
    print("49. Smallest Range:", smallest_range_k_lists([[4,10,15,24,26],[0,9,12,20],[5,18,22,30]])) 
 
    ro = reorganize_string("aab")
    valid = all(ro[i] != ro[i+1] for i in range(len(ro)-1)) and sorted(ro) == sorted("aab")
    print("50. Reorganize 'aab' ->", ro, "| valid:", valid)  
    print("50. Reorganize 'aaab' (impossible):", repr(reorganize_string("aaab")))  
 
    print("51. Least Interval (formula):", least_interval(["A","A","A","B","B","B"], 2))       
    print("51. Least Interval (simulation):", least_interval_simulation(["A","A","A","B","B","B"], 2))  
 
    import random
    random.seed(0)
    mismatches = 0
    for _ in range(300):
        tasks = [random.choice("ABCDE") for _ in range(random.randint(1, 15))]
        n = random.randint(0, 5)
        if least_interval(tasks, n) != least_interval_simulation(tasks, n):
            mismatches += 1
    print("51. Formula vs simulation mismatches over 300 random trials:", mismatches)  
 
