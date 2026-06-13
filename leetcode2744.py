# 2744. Find Maximum Number of String Pairs

class Solution(object):
    def maximumNumberOfStringPairs(self, words):
        """
        :type words: List[str]
        :rtype: int
        """
        count = 0
        for i in words:
            if i[::-1] in words and i != i[::-1]:
                count += 1

        return count//2
        

# class Solution(object):
#     def maximumNumberOfStringPairs(self, words):
#         count = 0
#         word = []
#         for i in words:
#             word.append(sorted(i))
#         for i in word:
#             if word.count(i) == 2:
#                 count += 1
#         return count//2

# class Solution(object):
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