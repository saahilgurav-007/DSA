from typing import List, Optional
from collections import defaultdict, deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val 
        self.left = left
        self.right = right

def build_tree_level_order(values: List[Optional[int]]) -> Optional[TreeNode]:
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    return root

# ---------------------------------------------------------------------------
# 35. Serialize and Deserialize Binary Tree
# ---------------------------------------------------------------------------
def serialize(root: Optional[TreeNode]) -> str:
    parts = []

    def preorder(node):
        if not node:
            parts.append('#')
            return
        parts.append(str(node.val))
        preorder(node.left)
        preorder(node.right)
    preorder(root)
    return ','.join(parts)


def deserialize(data: str) -> Optional[TreeNode]:
    tokens = iter(data.split(','))

    def build():
        val = next(tokens)
        if val == '#':
            return None
        node = TreeNode(int(val))
        node.left = build()
        node.right = build()
        return node
    return build()

# ---------------------------------------------------------------------------
# 36. Binary Tree Maximum Path Sum
# ---------------------------------------------------------------------------
def max_path_sum(root: Optional[TreeNode]) -> int:
    best = float('-inf')

    def dfs(node):
        nonlocal best
        if not node:
            return 0
        left_gain = max(dfs(node.left), 0)
        right_gain = max(dfs(node.right), 0)
        best = max(best, node.val + left_gain + right_gain)
        return node.val + max(left_gain, right_gain)
    dfs(root)
    return best

# ---------------------------------------------------------------------------
# 37. Construct Binary Tree from Preorder and Inorder Traversal
# ---------------------------------------------------------------------------
def build_tree_pre_in(preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
    index_in_inorder = {val: i for i, val in enumerate(inorder)}
    self_pre_idx = [0]  
 
    def helper(left: int, right: int) -> Optional[TreeNode]:
        if left > right:
            return None
        root_val = preorder[self_pre_idx[0]]
        self_pre_idx[0] += 1
        root = TreeNode(root_val)
        mid = index_in_inorder[root_val]
        root.left = helper(left, mid - 1)
        root.right = helper(mid + 1, right)
        return root
 
    return helper(0, len(inorder) - 1)
 
 
# ---------------------------------------------------------------------------
# 39. Vertical Order Traversal
# ---------------------------------------------------------------------------
def vertical_order_traversal(root: Optional[TreeNode]) -> List[List[int]]:
    if not root:
        return []
 
    columns = defaultdict(list)  
    queue = deque([(root, 0, 0)])  
 
    while queue:
        node, row, col = queue.popleft()
        columns[col].append((row, node.val))
        if node.left:
            queue.append((node.left, row + 1, col - 1))
        if node.right:
            queue.append((node.right, row + 1, col + 1))
 
    result = []
    for col in sorted(columns.keys()):
        entries = sorted(columns[col])  
        result.append([val for _, val in entries])
 
    return result
 
 
# ---------------------------------------------------------------------------
# 41. Lowest Common Ancestor (generic binary tree, not necessarily BST)
# ---------------------------------------------------------------------------
def lowest_common_ancestor(root: Optional[TreeNode], p: TreeNode, q: TreeNode) -> Optional[TreeNode]:
    if not root or root is p or root is q:
        return root
 
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
 
    if left and right:
        return root
    return left if left else right
 
 
# ---------------------------------------------------------------------------
# 42. Kth Smallest Element in BST
# ---------------------------------------------------------------------------
def kth_smallest_in_bst(root: Optional[TreeNode], k: int) -> int:
    stack = []
    node = root
 
    while stack or node:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        k -= 1
        if k == 0:
            return node.val
        node = node.right
 
    raise ValueError("k is larger than the number of nodes in the tree")
 
 
# ---------------------------------------------------------------------------
# 43. Recover Swapped BST (exactly two nodes swapped by mistake)
# ---------------------------------------------------------------------------
def recover_bst(root: Optional[TreeNode]) -> None:
    first = second = prev = None
 
    def inorder(node):
        nonlocal first, second, prev
        if not node:
            return
        inorder(node.left)
        if prev and prev.val > node.val:
            if first is None:
                first = prev
            second = node
        prev = node
        inorder(node.right)
 
    inorder(root)
    if first and second:
        first.val, second.val = second.val, first.val
 
 
# ---------------------------------------------------------------------------
# 44. Count Nodes in a Complete Binary Tree
# ---------------------------------------------------------------------------
def count_complete_tree_nodes(root: Optional[TreeNode]) -> int:
    if not root:
        return 0
 
    def height_left(node):
        h = 0
        while node:
            h += 1
            node = node.left
        return h
 
    def height_right(node):
        h = 0
        while node:
            h += 1
            node = node.right
        return h
 
    lh = height_left(root)
    rh = height_right(root)
 
    if lh == rh:
        return (1 << lh) - 1
 
    return 1 + count_complete_tree_nodes(root.left) + count_complete_tree_nodes(root.right)
 
 
# ---------------------------------------------------------------------------
# Self-tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    t35 = build_tree_level_order([1, 2, 3, None, None, 4, 5])
    s = serialize(t35)
    t35_back = deserialize(s)
    print("35. Serialize/Deserialize round-trip matches:", serialize(t35_back) == s)  
 
    t36 = build_tree_level_order([-10, 9, 20, None, None, 15, 7])
    print("36. Max Path Sum:", max_path_sum(t36))  # 42
 
    preorder, inorder = [3, 9, 20, 15, 7], [9, 3, 15, 20, 7]
    t37 = build_tree_pre_in(preorder, inorder)
    print("37. Rebuilt tree matches original serialization:", serialize(t37) == serialize(build_tree_level_order([3,9,20,None,None,15,7])))  
 
    t39 = build_tree_level_order([3, 9, 20, None, None, 15, 7])
    print("39. Vertical Order Traversal:", vertical_order_traversal(t39))  
 
    # 41. LCA
    t41 = build_tree_level_order([3,5,1,6,2,0,8,None,None,7,4])
    node5 = t41.left            
    node4 = t41.left.right.right  
    lca = lowest_common_ancestor(t41, node5, node4)
    print("41. LCA value:", lca.val) 
 
    t42 = build_tree_level_order([5, 3, 6, 2, 4, None, None, 1])
    print("42. Kth Smallest (k=3):", kth_smallest_in_bst(t42, 3))  # 3
 
    
    swapped = build_tree_level_order([3, 2, 1]) 
    root43 = TreeNode(2, TreeNode(3), TreeNode(1))
    recover_bst(root43)
    print("43. Recovered BST (inorder):", [root43.left.val, root43.val, root43.right.val])  # [1,2,3]
 
    t44 = build_tree_level_order([1,2,3,4,5,6])
    print("44. Count Complete Tree Nodes:", count_complete_tree_nodes(t44))