from platform import node
from typing import List

# ---------------------------------------------------------------------------
# 96. Trie-based Autocomplete System
# ---------------------------------------------------------------------------
class _AutocompleteTrieNode:
    __sloted__ = ('children', 'sentence_counts')
    def __init__(self):
        self.children = {}
        self.sentence_counts = {}

class AutocompleteSystem:
    def __init__(self, sentences: List[str], times: List[int]):
        self.root = _AutocompleteTrieNode()
        for sentence, count in zip(sentences, times):
            self._insert(sentence, count)
        self.current_input = ""

    def _insert(self, sentence: str, count: int) -> None:
        node  = self.root
        node.sentence_counts[sentence] = node.sentence_counts.get(sentence, 0) + count
        for ch in sentence:
            node = node.children.setdefault(ch, _AutocompleteTrieNode())
            node.sentence_counts[sentence] = node.sentence_counts.get(sentence, 0) + count

    def input(self, c:  str) -> List[str]:
        if c == '#':
            self._insert(self.current_input, 1)
            self.current_input = ""
            return []

        self.current_input += c
        node = self.root
        for ch in self.current_input:
            if ch not in node.children:
                return []  
            node = node.children[ch]
 
        candidates = sorted(node.sentence_counts.items(), key=lambda kv: (-kv[1], kv[0]))
        return [sentence for sentence, _ in candidates[:3]]

# ---------------------------------------------------------------------------
# 97. KMP Pattern Matching
# ---------------------------------------------------------------------------
def kmp_search(text: str, pattern: str) -> List[int]:
    if not pattern:
        return list(range(len(text) + 1))
 
    m = len(pattern)
    lps = [0] * m
    length = 0
    i = 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length > 0:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1
 
    matches = []
    i = j = 0  # i: text index, j: pattern index
    n = len(text)
    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == m:
                matches.append(i - j)
                j = lps[j - 1]
        elif j > 0:
            j = lps[j - 1]
        else:
            i += 1
 
    return matches
 
 
# ---------------------------------------------------------------------------
# 99. Segment Tree with Lazy Propagation (range add, range sum)
# ---------------------------------------------------------------------------
class SegmentTreeLazy:
    def __init__(self, arr: List[int]):
        self.n = len(arr)
        self.tree = [0] * (4 * self.n)
        self.lazy = [0] * (4 * self.n)
        self._build(arr, 0, 0, self.n - 1)
 
    def _build(self, arr, node, start, end):
        if start == end:
            self.tree[node] = arr[start]
            return
        mid = (start + end) // 2
        self._build(arr, 2 * node + 1, start, mid)
        self._build(arr, 2 * node + 2, mid + 1, end)
        self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]
 
    def _push_down(self, node, start, end):
        if self.lazy[node] != 0:
            mid = (start + end) // 2
            left, right = 2 * node + 1, 2 * node + 2
            for child, cs, ce in ((left, start, mid), (right, mid + 1, end)):
                self.tree[child] += self.lazy[node] * (ce - cs + 1)
                self.lazy[child] += self.lazy[node]
            self.lazy[node] = 0
 
    def update_range(self, l, r, val, node=0, start=None, end=None):
        if start is None:
            start, end = 0, self.n - 1
        if r < start or end < l:
            return
        if l <= start and end <= r:
            self.tree[node] += val * (end - start + 1)
            self.lazy[node] += val
            return
        self._push_down(node, start, end)
        mid = (start + end) // 2
        self.update_range(l, r, val, 2 * node + 1, start, mid)
        self.update_range(l, r, val, 2 * node + 2, mid + 1, end)
        self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]
 
    def query_range(self, l, r, node=0, start=None, end=None):
        if start is None:
            start, end = 0, self.n - 1
        if r < start or end < l:
            return 0
        if l <= start and end <= r:
            return self.tree[node]
        self._push_down(node, start, end)
        mid = (start + end) // 2
        return (self.query_range(l, r, 2 * node + 1, start, mid) +
                self.query_range(l, r, 2 * node + 2, mid + 1, end))
 
 
# ---------------------------------------------------------------------------
# 100. Fenwick Tree (BIT) for Range Update and Range Query
# ---------------------------------------------------------------------------
class FenwickRangeUpdateRangeQuery:
    def __init__(self, n: int):
        self.n = n
        self.B1 = [0] * (n + 2)
        self.B2 = [0] * (n + 2)
 
    def _add(self, bit, i, delta):
       
        while i <= self.n:
            bit[i] += delta
            i += i & (-i)
 
    def _sum(self, bit, i):
       
        total = 0
        while i > 0:
            total += bit[i]
            i -= i & (-i)
        return total
 
    def range_add(self, l: int, r: int, val: int) -> None:
       
        L, R = l + 1, r + 1
        self._add(self.B1, L, val)
        self._add(self.B1, R + 1, -val)
        self._add(self.B2, L, val * (L - 1))
        self._add(self.B2, R + 1, -val * R)
 
    def _prefix(self, i_zero_indexed: int) -> int:
        
        I = i_zero_indexed + 1  
        return self._sum(self.B1, I) * I - self._sum(self.B2, I)
 
    def range_sum(self, l: int, r: int) -> int:
        if l == 0:
            return self._prefix(r)
        return self._prefix(r) - self._prefix(l - 1)
 
# ---------------------------------------------------------------------------
# Self-tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    ac = AutocompleteSystem(["i love you", "island", "ironman", "i love leetcode"], [5, 3, 2, 2])
    print("96. input('i'):", ac.input('i'))         
    print("96. input(' '):", ac.input(' '))         
    print("96. input('a'):", ac.input('a'))          
    print("96. input('#'):", ac.input('#'))          
 
    ac2 = AutocompleteSystem(["i love you", "island", "ironman", "i love leetcode"], [5, 3, 2, 2])
    for ch in "i a": ac2.input(ch)
    ac2.input('#') 
    result = []
    for ch in "i a": result = ac2.input(ch)
    print("96. 'i a' now appears after re-typing:", 'i a' in result) 

    print("97. KMP matches:", kmp_search("ABABDABACDABABCABAB", "ABABCABAB"))  
    print("97. KMP no match:", kmp_search("AAAA", "AB"))                     
    print("97. KMP empty pattern:", kmp_search("AB", ""))                     
 
    arr = [1, 3, 5, 7, 9, 11]
    seg = SegmentTreeLazy(arr)
    print("99. Initial sum [1,3]:", seg.query_range(1, 3)) 
    seg.update_range(1, 3, 10) 
    print("99. Sum [1,3] after +10 range update:", seg.query_range(1, 3)) 
    print("99. Sum [0,5] after update:", seg.query_range(0, 5))           
 
    fen = FenwickRangeUpdateRangeQuery(6)
    for i, v in enumerate(arr):
        fen.range_add(i, i, v)  
    print("100. Initial sum [1,3]:", fen.range_sum(1, 3))  
    fen.range_add(1, 3, 10)
    print("100. Sum [1,3] after +10 range update:", fen.range_sum(1, 3)) 
    print("100. Sum [0,5] after update:", fen.range_sum(0, 5))