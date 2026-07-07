# 2657. Find the Prefix Common Array of Two Arrays

class Solution(object):
    def findThePrefixCommonArray(self, A, B):
        """
        :type A: List[int]
        :type B: List[int]
        :rtype: List[int]
        """
        hash = [0]*(len(A)+1)
        C = []
        for i in range(len(A)):
            hash[A[i]] += 1
            hash[B[i]] += 1
            C.append(hash.count(2))
        return C
s = Solution()
print(s.findThePrefixCommonArray([1,3,2,4],[3,1,2,4]))
            
# class Solution(object):
#     def findThePrefixCommonArray(self, A, B):
#         n = len(A)

#         freq = [0] * (n + 1)
#         ans = []
#         common = 0

#         for i in range(n):

#             freq[A[i]] += 1
#             if freq[A[i]] == 2:
#                 common += 1

#             freq[B[i]] += 1
#             if freq[B[i]] == 2:
#                 common += 1

#             ans.append(common)

#         return ans