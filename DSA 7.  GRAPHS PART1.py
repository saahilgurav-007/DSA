from typing import List, Dict, Tuple, Optional
import heapq
from collections import defaultdict, deque

# ---------------------------------------------------------------------------
# 52. Dijkstra's Algorithm with Path Reconstruction
# ---------------------------------------------------------------------------
def dijkstra_with_path(graph: Dict[int, List[Tuple[int, int]]], source: int, target: int):
    dist = {source: 0}
    prev = {}
    visited = set()
    heap = [(0, source)]

    while heapq:
        d, u = heapq.heappop(heap)
        if u in visited:
            continue
        visited.add(u)

        for v, w in graph.get(u, []):
            nd = d + w
            if v not in dist or nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(heap, (nd, v))
        if target not in dist:
            return float('-inf'), []

        path = [target]
        while path[-1] != source:
            path.append(prev[path[-1]])
        path.reverse()
        return dist[target], path
#---------------------------------------------------------------------------
# 53. Bellman-Ford with Negative Cycle Detection   
# ---------------------------------------------------------------------------
def bellman_ford(edges: List[Tuple[int, int, int]], n: int, source: int):
    dist = [float('-inf')] * n
    dist[source] = 0

    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] != float('-inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    has_negative_cycle = False
    for u, v, w in edges:
        if dist[u] != float('-inf') and dist[u] + w < dist[v]:
            has_negative_cycle = True
            break
    return dist, has_negative_cycle

# ---------------------------------------------------------------------------
# 54. Floyd-Warshall with Path Reconstruction
# ---------------------------------------------------------------------------
def floyd_warshall(dist_matrix: List[List[float]]):
    n = len(dist_matrix)
    dist = [row[:] for row in dist_matrix]
    nxt = [[j if dist[i][j] != float('inf') and i != j else None for j in range(n)] for i in range(n)]
 
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    nxt[i][j] = nxt[i][k]
 
    def reconstruct_path(i: int, j: int) -> List[int]:
        if nxt[i][j] is None:
            return []
        path = [i]
        while i != j:
            i = nxt[i][j]
            path.append(i)
        return path
 
    return dist, reconstruct_path
 
 
# ---------------------------------------------------------------------------
# 55. Topological Sort with Cycle Detection
# ---------------------------------------------------------------------------
def topological_sort(graph: Dict[int, List[int]], num_nodes: int):
    indegree = [0] * num_nodes
    for u in graph:
        for v in graph[u]:
            indegree[v] += 1
 
    queue = deque(u for u in range(num_nodes) if indegree[u] == 0)
    order = []
 
    while queue:
        u = queue.popleft()
        order.append(u)
        for v in graph.get(u, []):
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)
 
    has_cycle = len(order) != num_nodes
    return order, has_cycle
 
 
# ---------------------------------------------------------------------------
# 56. Course Schedule II
# ---------------------------------------------------------------------------
def find_order(num_courses: int, prerequisites: List[List[int]]) -> List[int]:
    graph = defaultdict(list)
    indegree = [0] * num_courses
 
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        indegree[course] += 1
 
    queue = deque(c for c in range(num_courses) if indegree[c] == 0)
    order = []
 
    while queue:
        u = queue.popleft()
        order.append(u)
        for v in graph[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)
 
    return order if len(order) == num_courses else []
 
 
# ---------------------------------------------------------------------------
# 58. Minimum Spanning Tree using Kruskal's Algorithm
# ---------------------------------------------------------------------------
class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n
 
    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  
        return self.parent[x]
 
    def union(self, x: int, y: int) -> bool:
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False   
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        return True
 
 
def kruskal_mst(n: int, edges: List[Tuple[int, int, int]]):
    edges_sorted = sorted(edges, key=lambda e: e[2])
    uf = UnionFind(n)
    total_weight = 0
    mst_edges = []
 
    for u, v, w in edges_sorted:
        if uf.union(u, v):
            total_weight += w
            mst_edges.append((u, v, w))
            if len(mst_edges) == n - 1:
                break
 
    return total_weight, mst_edges
 
 
# ---------------------------------------------------------------------------
# 59. Minimum Spanning Tree using Prim's Algorithm
# ---------------------------------------------------------------------------
def prim_mst(n: int, graph: Dict[int, List[Tuple[int, int]]], start: int = 0):
    visited = [False] * n
    heap = [(0, start, -1)]  
    total_weight = 0
    mst_edges = []
 
    while heap and len(mst_edges) < n - 1 + (1 if not visited[start] else 0):
        w, u, parent = heapq.heappop(heap)
        if visited[u]:
            continue
        visited[u] = True
        total_weight += w
        if parent != -1:
            mst_edges.append((parent, u, w))
 
        for v, weight in graph.get(u, []):
            if not visited[v]:
                heapq.heappush(heap, (weight, v, u))
 
    return total_weight, mst_edges
 
 

if __name__ == "__main__":
    
    graph52 = {0: [(1, 4), (2, 1)], 1: [(3, 1)], 2: [(1, 2), (3, 5)], 3: []}
    dist, path = dijkstra_with_path(graph52, 0, 3)
    print("52. Dijkstra dist/path:", dist, path) 
 
    
    edges53_ok = [(0, 1, 1), (1, 2, 3), (2, 3, 2), (0, 2, 5)]
    print("53. Bellman-Ford (no cycle):", bellman_ford(edges53_ok, 4, 0))  
 
    edges53_neg = [(0, 1, 1), (1, 2, -3), (2, 0, 1)]
    print("53. Bellman-Ford (negative cycle):", bellman_ford(edges53_neg, 3, 0)[1])  
 
    
    INF = float('inf')
    matrix54 = [
        [0, 4, 1, INF],
        [INF, 0, INF, 1],
        [INF, 2, 0, 5],
        [INF, INF, INF, 0],
    ]
    dist54, reconstruct = floyd_warshall(matrix54)
    print("54. Floyd-Warshall dist[0][3]:", dist54[0][3])           
    print("54. Floyd-Warshall path 0->3:", reconstruct(0, 3))       
 
    
    graph55 = {0: [1, 2], 1: [3], 2: [3], 3: [4], 4: []}
    print("55. Topo sort (valid DAG):", topological_sort(graph55, 5))  
 
    graph55_cycle = {0: [1], 1: [2], 2: [0]}
    print("55. Topo sort (cycle):", topological_sort(graph55_cycle, 3)[1]) 


    print("56. Course Schedule II:", find_order(4, [[1, 0], [2, 0], [3, 1], [3, 2]]))  
    print("56. Course Schedule II (impossible):", find_order(2, [[0, 1], [1, 0]]))     
 
    
    edges58 = [(0, 1, 10), (0, 2, 6), (0, 3, 5), (1, 3, 15), (2, 3, 4)]
    print("58. Kruskal MST weight:", kruskal_mst(4, edges58)[0])  
 
    
    graph59 = defaultdict(list)
    for u, v, w in edges58:
        graph59[u].append((v, w))
        graph59[v].append((u, w))
    print("59. Prim MST weight:", prim_mst(4, graph59, 0)[0])  