from typing import List, Optional
 
 
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
 
 
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
 
 
def build_tree_level_order(values):
    from collections import deque
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i]); queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i]); queue.append(node.right)
        i += 1
    return root
 
 
# ---------------------------------------------------------------------------
# 170. Add Two Numbers Represented by Linked Lists
# ---------------------------------------------------------------------------
def add_two_numbers(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
    dummy = ListNode()
    tail = dummy
    carry = 0
 
    while l1 or l2 or carry:
        v1 = l1.val if l1 else 0
        v2 = l2.val if l2 else 0
        total = v1 + v2 + carry
        carry, digit = divmod(total, 10)
        tail.next = ListNode(digit)
        tail = tail.next
        l1 = l1.next if l1 else None
        l2 = l2.next if l2 else None
 
    return dummy.next
 
 
def _list_to_python_list(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out
 
 
def _build_list(values):
    dummy = ListNode()
    cur = dummy
    for v in values:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next
 
 
# ---------------------------------------------------------------------------
# 178. MRU Cache (Most Recently Used eviction, opposite of LRU)
# ---------------------------------------------------------------------------
class _DLLNode:
    __slots__ = ('key', 'val', 'prev', 'next')
    def __init__(self, key=0, val=0):
        self.key = key; self.val = val; self.prev = None; self.next = None
 
 
class MRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.map = {}
        self.head = _DLLNode()
        self.tail = _DLLNode()
        self.head.next = self.tail
        self.tail.prev = self.head
 
    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev
 
    def _insert_after_head(self, node):
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
            mru = self.head.next
            self._remove(mru)
            del self.map[mru.key]
 
        node = _DLLNode(key, value)
        self.map[key] = node
        self._insert_after_head(node)
 
 
# ---------------------------------------------------------------------------
# 189. Morris Inorder Traversal (O(1) extra space, no stack/recursion)
# ---------------------------------------------------------------------------
def morris_inorder(root: Optional[TreeNode]) -> List[int]:
    result = []
    current = root
 
    while current:
        if not current.left:
            result.append(current.val)
            current = current.right
        else:
            predecessor = current.left
            while predecessor.right and predecessor.right is not current:
                predecessor = predecessor.right
 
            if predecessor.right is None:
                predecessor.right = current
                current = current.left
            else:
                predecessor.right = None
                result.append(current.val)
                current = current.right
 
    return result
 
 
# ---------------------------------------------------------------------------
# 201. Validate BST with Duplicate-Value Rules
# ---------------------------------------------------------------------------
def is_valid_bst_with_duplicates(root: Optional[TreeNode]) -> bool:
    def valid(node, low, high):
        if not node:
            return True
        if low is not None and node.val < low:
            return False
        if high is not None and node.val >= high:
            return False
        return valid(node.left, low, node.val) and valid(node.right, node.val, high)
 
    return valid(root, None, None)
 
 
# ---------------------------------------------------------------------------
# 208. BST Iterator with Bidirectional Traversal (next AND prev)
# ---------------------------------------------------------------------------
class BSTIteratorBidirectional:
    def __init__(self, root: Optional[TreeNode]):
        self.values = []
        self._inorder(root)
        self.pos = -1
 
    def _inorder(self, node):
        if not node:
            return
        self._inorder(node.left)
        self.values.append(node.val)
        self._inorder(node.right)
 
    def has_next(self) -> bool:
        return self.pos + 1 < len(self.values)
 
    def next(self) -> int:
        self.pos += 1
        return self.values[self.pos]
 
    def has_prev(self) -> bool:
        return self.pos > 0
 
    def prev(self) -> int:
        self.pos -= 1
        return self.values[self.pos]
 
 
# ---------------------------------------------------------------------------
# Self-tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    l1 = _build_list([2, 4, 3])  
    l2 = _build_list([5, 6, 4])  
    result = add_two_numbers(l1, l2)
    print("170. Add Two Numbers:", _list_to_python_list(result))  
 
    mru = MRUCache(2)
    mru.put(1, 1)
    mru.put(2, 2)
    print("178. MRU get(1):", mru.get(1))    
    mru.put(3, 3)                             
    print("178. MRU get(1):", mru.get(1))    
    print("178. MRU get(2):", mru.get(2))   
 
    t189 = build_tree_level_order([1, None, 2, 3])
    print("189. Morris Inorder:", morris_inorder(t189))  
   
    print("189. Morris Inorder (re-run, structure intact):", morris_inorder(t189))  
 
    t201_valid = build_tree_level_order([2, 1, 2])   
    t201_invalid = build_tree_level_order([2, 2, 3]) 
    print("201. Valid BST w/ dup rule (right-dup allowed):", is_valid_bst_with_duplicates(t201_valid))    # True
    print("201. Invalid BST w/ dup rule (left-dup disallowed):", is_valid_bst_with_duplicates(t201_invalid))  # False
 
    t208 = build_tree_level_order([7, 3, 15, None, None, 9, 20])
    it = BSTIteratorBidirectional(t208)
    seq = [it.next(), it.next(), it.has_next(), it.next(), it.prev(), it.prev()]
    print("208. BST Iterator sequence:", seq)