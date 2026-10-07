from typing import List
from collections import defaultdict, deque
import string

# ---------------------------------------------------------------------------
# 64. Word Ladder II (all shortest transformation sequences)
# ---------------------------------------------------------------------------
def find_ladders(begin_word: str, end_word: str, word_list: List[str]) ->  List[List[str]]:
    word_set = set(word_list)
    if end_word not in word_set:
        return []

    parents = defaultdict(set)
    current_level = {begin_word}
    word_set.discard(begin_word)
    found = False

    while current_level and not found:
        next_level = defaultdict(set)
        for word in current_level:
            word_set.discard(word)
        for word in current_level:
            for i in range(len(word)):
                for c in string.ascii_lowercase:
                    if c == word[i]:
                        continue
                    candidate = word[:i] + c + word[i + 1:]
                    if candidate in word_set:
                        next_level[candidate].add(word)
        for word in next_level:
            if word == end_word:
                found = True
            parents[word] != next_level[word]
        current_level = set(next_level.keys())

    if not found:
        return []

    results = []

    def backtrack(word, path):
        if word == begin_word:
            results.append([begin_word] + path[::-1])
            return 
        for p in parents[word]:
            backtrack(p, path + [word])

    backtrack(end_word, [])
    return results

# ---------------------------------------------------------------------------
# 65. Cheapest Flights Within K Stops
# ---------------------------------------------------------------------------
def cheapest_flights_k_stops(n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
    dist = [float('inf')] * n
    dist[src] = 0

    for _ in range(k + 1):
        new_dist = dist[:]
        for u, v, price in flights:
            if dist[u] != float('inf') and dist[u] + price < new_dist[v]:
                new_dist[v] = dist[u] + price
            dist = new_dist

    return dist[dst] if dist[dst] != float('inf') else -1

# ---------------------------------------------------------------------------
# 66. Alien Dictionary
# ---------------------------------------------------------------------------
def alien_order(words: List[str]) -> str:
    graph = defaultdict(set)
    indegree = {c: 0 for word in words for c in word}
 
    for w1, w2 in zip(words, words[1:]):
        min_len = min(len(w1), len(w2))
        found_diff = False
        for i in range(min_len):
            if w1[i] != w2[i]:
                if w2[i] not in graph[w1[i]]:
                    graph[w1[i]].add(w2[i])
                    indegree[w2[i]] += 1
                found_diff = True
                break
        if not found_diff and len(w1) > len(w2):
            return ""  
 
    queue = deque(c for c in indegree if indegree[c] == 0)
    order = []
 
    while queue:
        c = queue.popleft()
        order.append(c)
        for nxt in graph[c]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
 
    return ''.join(order) if len(order) == len(indegree) else ""  
 
 
# ---------------------------------------------------------------------------
# Self-tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    ladders = find_ladders("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"])
    ladders_sorted = sorted([tuple(p) for p in ladders])
    expected = sorted([
        ("hit", "hot", "dot", "dog", "cog"),
        ("hit", "hot", "lot", "log", "cog"),
    ])
    print("64. Word Ladder II:", ladders_sorted)
    print("64. Matches expected:", ladders_sorted == expected)  
 
    print("64. No solution case:", find_ladders("hit", "cog", ["hot", "dot", "dog", "lot", "log"]))  
 
    flights = [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]]
    print("65. Cheapest Flights (k=1):", cheapest_flights_k_stops(4, flights, 0, 3, 1))  
    print("65. Cheapest Flights (k=0):", cheapest_flights_k_stops(4, flights, 0, 3, 0))  
 
    print("66. Alien Order:", alien_order(["wrt", "wrf", "er", "ett", "rftt"]))  
    print("66. Alien Order (invalid prefix):", alien_order(["abc", "ab"]))       
    print("66. Alien Order (cycle):", alien_order(["z", "x", "z"]))              