# 3857. Minimum Cost to Split into Ones

class Solution(object):
    def minCost(self, n):
        return ((n)*(n-1))//2

# class Solution(object):
#     def minCost(self, n):
#         ans = 0
#         while n > 0:
#             ans += n - 1
#             n -= 1
#         return ans