from typing import List
# ---------------------------------------------------------------------------
# 74. Palindrome Partitioning II (minimum cuts)
# ---------------------------------------------------------------------------
def min_palindrome_cuts(s: str) -> int:
    n = len(s)
    is_pal = [[False] * n for _ in range(n)]
    for i in range(n):
        is_pal[i][i] = True
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j] and (length == 2 or is_pal[i + 1][j - 1]):
                is_pal[i][j] = True

    min_cuts = [0] * n
    for i in range(n):
        if is_pal[0][i]:
            min_cuts[i] = 0
            continue
        min_cuts[i] = i
        for j in range(1, i + 1):
            if is_pal[j][i]:
                min_cuts[i] = min(min_cuts[i], min_cuts[j - 1] + 1)

    return min_cuts[n - 1] if n > 0 else 0

# ---------------------------------------------------------------------------
# 75. Regular Expression Matching (supports '.' and '*')
# ---------------------------------------------------------------------------
def is_match_regex(s: str, p: str) -> bool:
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True
 
    for j in range(1, n + 1):
        if p[j - 1] == '*':
            dp[0][j] = dp[0][j - 2]
 
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j - 1] == '*':
                dp[i][j] = dp[i][j - 2]  
                prev = p[j - 2]
                if prev == '.' or prev == s[i - 1]:
                    dp[i][j] = dp[i][j] or dp[i - 1][j]  
            elif p[j - 1] == '.' or p[j - 1] == s[i - 1]:
                dp[i][j] = dp[i - 1][j - 1]
          
 
    return dp[m][n]
 
 
# ---------------------------------------------------------------------------
# 76. Wildcard Matching (supports '?' and '*')
# ---------------------------------------------------------------------------
def is_match_wildcard(s: str, p: str) -> bool:
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True
 
    for j in range(1, n + 1):
        if p[j - 1] == '*':
            dp[0][j] = dp[0][j - 1]
 
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j - 1] == '*':
                dp[i][j] = dp[i][j - 1] or dp[i - 1][j]
            elif p[j - 1] == '?' or p[j - 1] == s[i - 1]:
                dp[i][j] = dp[i - 1][j - 1]
 
    return dp[m][n]
 
 
# ---------------------------------------------------------------------------
# 77. Burst Balloons
# ---------------------------------------------------------------------------
def max_coins_burst_balloons(nums: List[int]) -> int:
    balloons = [1] + nums + [1]
    n = len(balloons)
    dp = [[0] * n for _ in range(n)]
 
    for length in range(2, n):  # length = distance between i and j
        for i in range(0, n - length):
            j = i + length
            for k in range(i + 1, j):
                dp[i][j] = max(
                    dp[i][j],
                    dp[i][k] + dp[k][j] + balloons[i] * balloons[k] * balloons[j]
                )
 
    return dp[0][n - 1]
 
 
# ---------------------------------------------------------------------------
# 80. Distinct Subsequences (count distinct subsequences of s equal to t)
# ---------------------------------------------------------------------------
def num_distinct_subsequences(s: str, t: str) -> int:
    m, n = len(s), len(t)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = 1 
 
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            dp[i][j] = dp[i - 1][j]  
            if s[i - 1] == t[j - 1]:
                dp[i][j] += dp[i - 1][j - 1]  
 
    return dp[m][n]
 
 
# ---------------------------------------------------------------------------
# Self-tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("74. Min Palindrome Cuts ('aab'):", min_palindrome_cuts("aab"))  
    print("74. Min Palindrome Cuts ('a'):", min_palindrome_cuts("a"))      
 
    print("75. Regex 'aa' vs 'a*':", is_match_regex("aa", "a*"))                          
    print("75. Regex 'mississippi' vs 'mis*is*p*.':", is_match_regex("mississippi", "mis*is*p*."))  
    print("75. Regex 'ab' vs '.*':", is_match_regex("ab", ".*"))                          
 
    print("76. Wildcard 'adceb' vs '*a*b':", is_match_wildcard("adceb", "*a*b"))  
    print("76. Wildcard 'acdcb' vs 'a*c?b':", is_match_wildcard("acdcb", "a*c?b"))  
 
    print("77. Burst Balloons [3,1,5,8]:", max_coins_burst_balloons([3, 1, 5, 8]))
 
    print("80. Distinct Subsequences ('rabbbit','rabbit'):", num_distinct_subsequences("rabbbit", "rabbit")) 