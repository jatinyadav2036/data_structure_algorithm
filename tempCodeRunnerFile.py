class Solution(object):
#     def maximumNumberOfStringPairs(self, words):
#         """
#         :type words: List[str]
#         :rtype: int
#         """
#         a = {}
#         for i in words:
#             if i[::-1] in a:
#                 a[i[::-1]] += 1
#             else:
#                 a[i] = 1
        
#         return len([i for i, j in a.items() if j == 2])