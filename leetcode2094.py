# 2094. Finding 3-Digit Even Numbers


from itertools import permutations
class Solution(object):
    def findEvenNumbers(self, digits):
        pairs = set(permutations(digits, 3))
        ans = []

        for a, b, c in pairs:
            if a != 0 and c % 2 == 0:
                ans.append(100 * a + 10 * b + c)

        return sorted(ans)
    


# class Solution(object):
#     def findEvenNumbers(self, digits):
#         from collections import Counter
#         count = Counter(digits)
#         res = set()
#         for i in range(100, 1000, 2):
#             a, b, c = i // 100, (i // 10) % 10, i % 10
#             need = Counter([a, b, c])
#             if need[a] <= count[a] and need[b] <= count[b] and need[c] <= count[c]:
#                 res.add(i)
#         return sorted(res)