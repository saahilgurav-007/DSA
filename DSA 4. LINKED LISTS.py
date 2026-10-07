from typing import List, Optional
import heapq

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class RandomNode:
    def __init__(self, val=0, next=None, random=None):
        self.val = val
        self.next = next
        self.random = random

def build_list(values: List[int]) -> Optional[ListNode]:
    dumpy = ListNode()
    cur = dumpy
    for v in values:
        cur.next = ListNode(v)
        cur = cur.next
    return dumpy.next

def to_list(head: Optional[ListNode]) -> List[int]:
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out

#---------------------------------------------------------------------------
# 27. Reverse Nodes in K-Group
#---------------------------------------------------------------------------
def reverse_k_group(head: Optional[ListNode], k: int) -> Optional[ListNode]:
    if k <= 0:
        raise ValueError("k must be greater than 0")
    node = head
    count = 0
    while node and count < k:
        node = node.next
        count += 1
    if count < k:
        return head

    prev, cur = None, head
    for _ in range(k):
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt

    head.next = reverse_k_group(cur, k)
    return prev

# ---------------------------------------------------------------------------
# 28. Merge K Sorted Linked Lists
# ---------------------------------------------------------------------------
def merge_k_sorted_lists(lists: List[Optional[ListNode]]) -> Optional[ListNode]:
    heap = []
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))

    dummy = ListNode()
    tail = dummy

    while heap:
        val, i, node = heapq.heappop(heap)
        tail.next = node
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
    return dummy.next

# ---------------------------------------------------------------------------
# 29. Copy List with Random Pointer
#---------------------------------------------------------------------------
def copy_random_list(head: Optional[RandomNode]) -> Optional[RandomNode]:
    if not head:
        return None
    node = head
    while node:
        clone = RandomNode(node.val, node.next, None)
        node.next = clone
        node = clone.next

    node = head
    while node:
        if node.random:
            node.next.random = node.random.next
        node = node.next.next

    node = head
    new_head = head.next
    while node:
        clone = node.next
        node.next = clone.next
        clone.next = clone.next.next if clone.next else None
        node = node.next

    return new_head

#---------------------------------------------------------------------------
# 31. Sort Linked List using Merge Sort
# ---------------------------------------------------------------------------
def sort_list(head: Optional[ListNode]) -> Optional[ListNode]:
    if not head or not head.next:
        return head

    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    mid = slow.next
    slow.next = None

    left = sort_list(head)
    right = sort_list(mid)

    dummy = ListNode()
    tail = dummy
    while left and right:
        if left.val <= right.val:
            tail.next, left = left, left.next
        else:
            tail.next, right = right, right.next
        tail = tail.next
    tail.next = left if left else right

    return dummy.next

# ---------------------------------------------------------------------------
# 32. Rotate Linked List
# ---------------------------------------------------------------------------
def rotate_right(head: Optional[ListNode], k: int) -> Optional[ListNode]:
    if not head or not head.next or k == 0:
        return head

    length = 1
    tail = head
    while tail.next:
        tail = tail.next
        length += 1

    k %= length
    if k == 0:
        return head

    tail.next = head
    steps_to_new_tail = length - k - 1
    new_tail = head 
    for _ in range(steps_to_new_tail):
        new_tail = new_tail.next

    new_head = new_tail.next
    new_tail.next = None
    return new_head
# ---------------------------------------------------------------------------
# 33. Find Intersection of Two Linked Lists
# ---------------------------------------------------------------------------
def get_intersection_node(
    headA: Optional[ListNode],
    headB: Optional[ListNode]
) -> Optional[ListNode]:

    if not headA or not headB:
        return None

    a, b = headA, headB

    while a is not b:
        a = a.next if a else headB
        b = b.next if b else headA

    return a
#---------------------------------------------------------------------------
# 34. Design an LRU Cache using Doubly Linked List + Hash Map
#---------------------------------------------------------------------------
class DLLNode:
    __slots__ = ('key', 'val', 'prev', 'next')
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be greater than 0")
        self.capacity = capacity
        self.map = {}
        self.head = DLLNode()
        self.tail = DLLNode()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: DLLNode) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev
 
    def _insert_after_head(self, node: DLLNode) -> None:
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node
 
    def get(self, key: int) -> int:
        if key not in self.map:
            return -1
        node = self.map[key]
        self._remove(node)
        self._insert_after_head(node)
        return node.val
 
    def put(self, key: int, value: int) -> None:
        if key in self.map:
            node = self.map[key]
            node.val = value
            self._remove(node)
            self._insert_after_head(node)
            return
 
        if len(self.map) >= self.capacity:
            lru = self.tail.prev
            self._remove(lru)
            del self.map[lru.key]
 
        node = DLLNode(key, value)
        self.map[key] = node
        self._insert_after_head(node)
 
 
# ---------------------------------------------------------------------------
# Self-tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("27. Reverse K-Group:", to_list(reverse_k_group(build_list([1,2,3,4,5]), 2)))  
 
    l1, l2, l3 = build_list([1,4,5]), build_list([1,3,4]), build_list([2,6])
    print("28. Merge K Sorted Lists:", to_list(merge_k_sorted_lists([l1, l2, l3])))    
 
    
    n1, n2 = RandomNode(1), RandomNode(2)
    n1.next = n2
    n1.random = n2
    n2.random = n1
    copy_head = copy_random_list(n1)
    print("29. Copy Random List vals:", [copy_head.val, copy_head.next.val])              
    print("29. Copy Random correctness:", copy_head.random is copy_head.next,             
          copy_head.next.random is copy_head)                                              
    print("29. Original untouched (deep copy check):", copy_head is not n1, copy_head.next is not n2)  
 
    print("31. Sort List (merge sort):", to_list(sort_list(build_list([4,2,1,3]))))        
    print("32. Rotate Right by 2:", to_list(rotate_right(build_list([1,2,3,4,5]), 2)))   
 
    
    common = build_list([8, 4, 5])
    a = build_list([4, 1])
    b = build_list([5, 6, 1])
    node = a
    while node.next:
        node = node.next
    node.next = common
    node = b
    while node.next:
        node = node.next
    node.next = common
    inter = get_intersection_node(a, b)
    print("33. Intersection value:", inter.val if inter else None)                         # 8
 
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    print("34. LRU get(1):", cache.get(1))  
    cache.put(3, 3)                          
    print("34. LRU get(2):", cache.get(2))   
    cache.put(4, 4)                          
    print("34. LRU get(1):", cache.get(1))   
    print("34. LRU get(3):", cache.get(3))   
    print("34. LRU get(4):", cache.get(4))   
  
