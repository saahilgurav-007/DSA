from typing import List
import heapq
from collections import deque, defaultdict
 
 
# ---------------------------------------------------------------------------
# 225. Kth Smallest Pair Distance
# ---------------------------------------------------------------------------
def kth_smallest_pair_distance(nums: List[int], k: int) -> int:
    nums.sort()
    n = len(nums)
 
    def count_pairs_within(d: int) -> int:
        count = 0
        left = 0
        for right in range(n):
            while nums[right] - nums[left] > d:
                left += 1
            count += right - left
        return count
 
    lo, hi = 0, nums[-1] - nums[0]
    while lo < hi:
        mid = (lo + hi) // 2
        if count_pairs_within(mid) >= k:
            hi = mid
        else:
            lo = mid + 1
 
    return lo
 
 
# ---------------------------------------------------------------------------
# 234. Minimum Cost to Connect All Ropes
# ---------------------------------------------------------------------------
def min_cost_connect_ropes(ropes: List[int]) -> int:
    if len(ropes) <= 1:
        return 0
 
    heap = ropes[:]
    heapq.heapify(heap)
    total_cost = 0
 
    while len(heap) > 1:
        first = heapq.heappop(heap)
        second = heapq.heappop(heap)
        cost = first + second
        total_cost += cost
        heapq.heappush(heap, cost)
 
    return total_cost
 
 
# ---------------------------------------------------------------------------
# 245. Rotting Oranges with Multiple Speeds
# ---------------------------------------------------------------------------
def rotting_oranges_multi_speed(grid: List[List[int]], speed_map: dict = None) -> int:
    rows, cols = len(grid), len(grid[0])
    default_speed = 1
    speed_map = speed_map or {}
 
    dist = [[-1] * cols for _ in range(rows)]
    heap = []
    fresh_count = 0
 
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                dist[r][c] = 0
                heapq.heappush(heap, (0, r, c))
            elif grid[r][c] == 1:
                fresh_count += 1
 
    if fresh_count == 0:
        return 0
 
    max_time = 0
    infected = 0
 
    while heap:
        time, r, c = heapq.heappop(heap)
        if time > dist[r][c]:
            continue
 
        speed = speed_map.get((r, c), default_speed)
 
        for dr, dc in ((1,0), (-1,0), (0,1), (0,-1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                new_time = time + speed
                if dist[nr][nc] == -1 or new_time < dist[nr][nc]:
                    if dist[nr][nc] == -1:
                        infected += 1
                    dist[nr][nc] = new_time
                    max_time = max(max_time, new_time)
                    heapq.heappush(heap, (new_time, nr, nc))
 
    return max_time if infected == fresh_count else -1
 
 
# ---------------------------------------------------------------------------
# 246. Shortest Path in a Binary Matrix with Obstacles
# ---------------------------------------------------------------------------
def shortest_path_binary_matrix(grid: List[List[int]]) -> int:
    n = len(grid)
    if grid[0][0] == 1 or grid[n-1][n-1] == 1:
        return -1
 
    directions = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    visited = [[False]*n for _ in range(n)]
    visited[0][0] = True
    queue = deque([(0, 0, 1)])
 
    while queue:
        r, c, dist = queue.popleft()
        if r == n-1 and c == n-1:
            return dist
        for dr, dc in directions:
            nr, nc = r+dr, c+dc
            if 0 <= nr < n and 0 <= nc < n and not visited[nr][nc] and grid[nr][nc] == 0:
                visited[nr][nc] = True
                queue.append((nr, nc, dist+1))
 
    return -1
 
 
# ---------------------------------------------------------------------------
# 297. Lowest Common Ancestor with Binary Lifting
# ---------------------------------------------------------------------------
class LCABinaryLifting:
    def __init__(self, n: int, edges: List[List[int]], root: int = 0):
        self.n = n
        self.LOG = max(1, (n).bit_length())
        self.up = [[-1] * n for _ in range(self.LOG)]
        self.depth = [0] * n
 
        graph = defaultdict(list)
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)
 
        visited = [False] * n
        visited[root] = True
        queue = deque([root])
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                if not visited[v]:
                    visited[v] = True
                    self.up[0][v] = u
                    self.depth[v] = self.depth[u] + 1
                    queue.append(v)
 
        for k in range(1, self.LOG):
            for v in range(n):
                if self.up[k-1][v] != -1:
                    self.up[k][v] = self.up[k-1][self.up[k-1][v]]
 
    def lca(self, u: int, v: int) -> int:
        if self.depth[u] < self.depth[v]:
            u, v = v, u
 
        diff = self.depth[u] - self.depth[v]
        for k in range(self.LOG):
            if (diff >> k) & 1:
                u = self.up[k][u]
 
        if u == v:
            return u
 
        for k in range(self.LOG - 1, -1, -1):
            if self.up[k][u] != -1 and self.up[k][u] != self.up[k][v]:
                u = self.up[k][u]
                v = self.up[k][v]
 
        return self.up[0][u]
 
 
# ---------------------------------------------------------------------------
# Self-tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("225. Kth Smallest Pair Distance [1,3,1], k=1:", kth_smallest_pair_distance([1, 3, 1], 1))  
    print("225. Kth Smallest Pair Distance [1,1,1], k=2:", kth_smallest_pair_distance([1, 1, 1], 2))  
 
    print("234. Min Cost Connect Ropes [4,3,2,6]:", min_cost_connect_ropes([4, 3, 2, 6]))  
 
    grid245 = [
        [2, 1, 1],
        [1, 1, 0],
        [0, 1, 1],
    ]
    print("245. Rotting Oranges, uniform speed:", rotting_oranges_multi_speed(grid245))  
    print("245. Rotting Oranges, fast rotten at (0,0) speed=1 for all (default):",
          rotting_oranges_multi_speed(grid245, speed_map={(0,0): 1})) 
    grid245_unreachable = [[2,1,0],[0,0,1],[0,1,1]]  
    print("245. Rotting Oranges, unreachable fresh:", rotting_oranges_multi_speed(grid245_unreachable))  
 
    grid246 = [[0,0,0],[1,1,0],[1,1,0]]
    print("246. Shortest Path Binary Matrix:", shortest_path_binary_matrix(grid246))  
    grid246_blocked = [[0,1],[1,0]]
    print("246. Shortest Path Binary Matrix (diagonal squeeze-through):",
          shortest_path_binary_matrix(grid246_blocked))  
    grid246_truly_blocked = [[0,1,1],[1,1,1],[1,1,0]]  
    print("246. Shortest Path Binary Matrix (truly no path):",
          shortest_path_binary_matrix(grid246_truly_blocked)) 
 
    
    edges297 = [[0,1],[0,2],[1,3],[1,4],[2,5],[2,6]]
    lca_solver = LCABinaryLifting(7, edges297, root=0)
    print("297. LCA(3,4):", lca_solver.lca(3, 4))  
    print("297. LCA(3,5):", lca_solver.lca(3, 5)) 
    print("297. LCA(5,6):", lca_solver.lca(5, 6))