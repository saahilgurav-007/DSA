from typing import List, Optional
 
 
# ---------------------------------------------------------------------------
# 143. Online Stock Span with Historical Queries
# ---------------------------------------------------------------------------
class StockSpanner:
    def __init__(self):
        self.stack = []
        self.history = []
 
    def next(self, price: int) -> int:
        span = 1
        while self.stack and self.stack[-1][0] <= price:
            span += self.stack.pop()[1]
        self.stack.append((price, span))
        self.history.append(span)
        return span
 
    def query_historical_span(self, day_index: int) -> int:
        """0-indexed day (0 = first call to next())."""
        if day_index < 0 or day_index >= len(self.history):
            raise IndexError("day_index out of range of recorded history")
        return self.history[day_index]
 
 
# ---------------------------------------------------------------------------
# 144. Online Next Greater Element (elements arrive one at a time, resolve
# earlier elements' "next greater" as soon as a bigger one shows up)
# ---------------------------------------------------------------------------
class OnlineNextGreaterElement:
    def __init__(self):
        self.results = []
        self.stack = []
 
    def push(self, val: int) -> List[int]:
        """Feeds the next value into the stream. Returns the list of
        (index, resolved_value) pairs that got resolved by THIS push."""
        idx = len(self.results)
        self.results.append(-1)
        resolved = []
 
        while self.stack and self.results[self.stack[-1]] == -1 and self._peek_value(self.stack[-1]) < val:
            j = self.stack.pop()
            self.results[j] = val
            resolved.append((j, val))
 
        self.stack.append(idx)
        self._values = getattr(self, '_values', [])
        self._values.append(val)
        return resolved
 
    def _peek_value(self, idx):
        return self._values[idx]
 
    def current_results(self) -> List[int]:
        """Snapshot of resolved-so-far next-greater values (-1 = not yet resolved)."""
        return self.results[:]
 
 
# ---------------------------------------------------------------------------
# 145. Next Greater Element in a Dynamic Array (supports appends)
# ---------------------------------------------------------------------------
class DynamicArrayNextGreater:
    def __init__(self):
        self.arr = []
        self.result = []
        self.stack = []
 
    def append(self, val: int) -> None:
        idx = len(self.arr)
        self.arr.append(val)
        self.result.append(-1)
 
        while self.stack and self.arr[self.stack[-1]] < val:
            j = self.stack.pop()
            self.result[j] = val
 
        self.stack.append(idx)
 
    def get_results(self) -> List[int]:
        return self.result[:]
 
 
# ---------------------------------------------------------------------------
# 146. Circular Next Greater Element
# ---------------------------------------------------------------------------
def next_greater_circular(nums: List[int]) -> List[int]:
    n = len(nums)
    result = [-1] * n
    stack = []
 
    for i in range(2 * n):
        actual_i = i % n
        while stack and nums[stack[-1]] < nums[actual_i]:
            result[stack.pop()] = nums[actual_i]
        if i < n:
            stack.append(actual_i)
 
    return result
 
 
# ---------------------------------------------------------------------------
# Self-tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    spanner = StockSpanner()
    prices = [100, 80, 60, 70, 60, 75, 85]
    spans = [spanner.next(p) for p in prices]
    print("143. Stock spans:", spans)  
    print("143. Historical query for day 5 (0-indexed):", spanner.query_historical_span(5))  
 
    ong = OnlineNextGreaterElement()
    stream = [4, 5, 2, 25]
    for v in stream:
        ong.push(v)
    print("144. Online Next Greater final results:", ong.current_results())  
 
    dyn = DynamicArrayNextGreater()
    for v in [4, 5, 2, 25]:
        dyn.append(v)
    print("145. Dynamic Array Next Greater:", dyn.get_results())  
 
    print("146. Circular Next Greater [1,2,1]:", next_greater_circular([1, 2, 1]))  
    print("146. Circular Next Greater [5,4,3,2,1]:", next_greater_circular([5, 4, 3, 2, 1]))  