# 1551. Minimum Operations to Make Array Equal

class Solution(object):
    def minOperations(self, n):
        arr = []
        for i in range(n):
            arr.append(2*i+1)
        target = sum(arr)//n
        cnt = 0
        for i in range(len(arr)//2):
            cnt += (target-arr[i])
        return cnt        

# class Solution(object):
#     def minOperations(self, n):
#         """
#         :type n: int
#         :rtype: int
#         """

#         return n*(n//2) - (n//2)**2