from typing import List
from collections import deque

# ---------------------------------------------------------------------------
# 85. N-Queens
# ---------------------------------------------------------------------------
def solve_n_queens(n: int) -> List[List[str]]:
    results = []
    cols, diag1, diag2 = set(), set(), set()
    board_cols = [-1] * n

    def backtrack(row: int):
        if row == n:
            board = []
            for r in range(n):
                line = ['.'] * n
                line[board_cols[r]] = 'Q'
                board.append(''.join(line))
            results.append(board)
            return

        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            cols.add(col); diag1.add(row - col); diag2.add(row + col)
            board_cols[row] = col
            backtrack(row + 1)
            cols.remove(col); diag1.remove(row - col); diag2.remove(row + col)

    backtrack(0)
    return results

# ---------------------------------------------------------------------------
# 86. Sudoku Solver
# FIX: function was named solve_suduko (typo) -> renamed to solve_sudoku
# to match the self-test call and standard naming.
# ---------------------------------------------------------------------------
def solve_sudoku(board: List[List[str]]) -> bool:
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]
    empties = []

    for r in range(9):
        for c in range(9):
            val = board[r][c]
            if val == '.':
                empties.append((r, c))
            else:
                rows[r].add(val)
                cols[c].add(val)
                boxes[(r // 3) * 3 + c // 3].add(val)

    def backtrack(idx: int) -> bool:
        if idx == len(empties):
            return True
        r, c = empties[idx]
        box_id = (r // 3) * 3 + c // 3

        for digit in '123456789':
            if digit in rows[r] or digit in cols[c] or digit in boxes[box_id]:
                continue
            board[r][c] = digit
            rows[r].add(digit); cols[c].add(digit); boxes[box_id].add(digit)

            if backtrack(idx + 1):
                return True

            board[r][c] = '.'
            rows[r].remove(digit); cols[c].remove(digit); boxes[box_id].remove(digit)

        return False
    return backtrack(0)

# ---------------------------------------------------------------------------
# 87. Word Search II using Trie
# ---------------------------------------------------------------------------
class TrieNode:
    __slots__ = ('children', 'word')
    def __init__(self):
        self.children = {}
        self.word = None

def find_words(board: List[List[str]], words: List[str]) -> List[str]:
    root = TrieNode()
    for word in words:
        node = root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.word = word

    rows, cols = len(board), len(board[0])
    found = []

    def dfs(r, c, node):
        ch = board[r][c]
        if ch not in node.children:
            return
        child = node.children[ch]
        if child.word:
            found.append(child.word)
            child.word = None

        board[r][c] = '#'
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != '#':
                dfs(nr, nc, child)
        board[r][c] = ch

        if not child.children:
            node.children.pop(ch, None)

    for r in range(rows):
        for c in range(cols):
            dfs(r, c, root)

    return found

# ---------------------------------------------------------------------------
# 88. Expression Add Operators
# ---------------------------------------------------------------------------
def add_operators(num: str, target: int) -> List[str]:
    results = []
    n = len(num)

    def backtrack(index, path, value, last_operand):
        if index == n:
            if value == target:
                results.append(path)
            return

        for end in range(index + 1, n + 1):
            part = num[index:end]
            if len(part) > 1 and part[0] == '0':
                break
            operand = int(part)

            if index == 0:
                backtrack(end, part, operand, operand)
            else:
                backtrack(end, path + '+' + part, value + operand, operand)
                backtrack(end, path + '-' + part, value - operand, -operand)
                backtrack(end, path + '*' + part,
                          value - last_operand + last_operand * operand,
                          last_operand * operand)

    backtrack(0, "", 0, 0)
    return results

# ---------------------------------------------------------------------------
# 89. Palindrome Partitioning — All Possible Partitions
# FIX: helper was named is_palidrome (typo) but called as is_palindrome
# -> renamed definition to is_palindrome so it actually resolves.
# ---------------------------------------------------------------------------
def palindrome_partitions(s: str) -> List[List[str]]:
    results = []
    n = len(s)

    def is_palindrome(sub: str) -> bool:
        return sub == sub[::-1]

    def backtrack(start, path):
        if start == n:
            results.append(path[:])
            return
        for end in range(start + 1, n + 1):
            substr = s[start:end]
            if is_palindrome(substr):
                path.append(substr)
                backtrack(end, path)
                path.pop()

    backtrack(0, [])
    return results


# ---------------------------------------------------------------------------
# 90. Remove Invalid Parentheses (return all valid results with minimum removals)
# ---------------------------------------------------------------------------
def remove_invalid_parentheses(s: str) -> List[str]:
    def is_valid(string: str) -> bool:
        balance = 0
        for ch in string:
            if ch == '(':
                balance += 1
            elif ch == ')':
                balance -= 1
                if balance < 0:
                    return False
        return balance == 0

    if is_valid(s):
        return [s]

    visited = {s}
    queue = deque([s])
    results = []
    found = False

    while queue and not found:
        level_size = len(queue)
        for _ in range(level_size):
            current = queue.popleft()
            for i in range(len(current)):
                if current[i] not in '()':
                    continue
                candidate = current[:i] + current[i + 1:]
                if candidate in visited:
                    continue
                visited.add(candidate)
                if is_valid(candidate):
                    results.append(candidate)
                    found = True
                else:
                    queue.append(candidate)

    return results if results else [""]

# ---------------------------------------------------------------------------
# Self-tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    solutions_4queens = solve_n_queens(4)
    print("85. N-Queens (n=4) solution count:", len(solutions_4queens))  # 2

    board86 = [
        ["5","3",".",".","7",".",".",".","."],
        ["6",".",".","1","9","5",".",".","."],
        [".","9","8",".",".",".",".","6","."],
        ["8",".",".",".","6",".",".",".","3"],
        ["4",".",".","8",".","3",".",".","1"],
        ["7",".",".",".","2",".",".",".","6"],
        [".","6",".",".",".",".","2","8","."],
        [".",".",".","4","1","9",".",".","5"],
        [".",".",".",".","8",".",".","7","9"],
    ]
    solved = solve_sudoku(board86)

    def valid_group(cells):
        return sorted(cells) == [str(d) for d in range(1, 10)]
    rows_ok = all(valid_group(row) for row in board86)
    cols_ok = all(valid_group([board86[r][c] for r in range(9)]) for c in range(9))
    boxes_ok = all(
        valid_group([board86[r][c] for r in range(br, br+3) for c in range(bc, bc+3)])
        for br in (0,3,6) for bc in (0,3,6)
    )
    print("86. Sudoku solved:", solved, "| rows/cols/boxes valid:", rows_ok, cols_ok, boxes_ok)

    board87 = [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]]
    words87 = ["oath","pea","eat","rain"]
    print("87. Word Search II:", sorted(find_words(board87, words87)))

    print("88. Add Operators ('123', 6):", sorted(add_operators("123", 6)))

    print("89. Palindrome Partitions ('aab'):", palindrome_partitions("aab"))

    result90 = remove_invalid_parentheses("()())()")
    all_valid = all(
        sum(1 if c=='(' else -1 if c==')' else 0 for c in r) == 0 and
        all(sum(1 if x=='(' else -1 for x in r[:i+1] if x in '()') >= 0 for i in range(len(r)))
        for r in result90
    )
    print("90. Remove Invalid Parentheses:", sorted(result90), "| all valid:", all_valid)